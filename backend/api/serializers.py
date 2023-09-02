import base64
from django.core.files.base import ContentFile
from djoser.serializers import (
    UserSerializer as DjoserUserSerializer,
    UserCreateSerializer as DjoserUserCreateSerializer
)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import (Ingredient, Tag, Recipe,
                            Favorite, ShoppingCart)
from users.models import Subscribe, User


class UserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, user):
        current_user = self.context.get('request').user
        return (current_user.is_authenticated
                and user.subscribed.filter(subscriber=current_user).exists())


class UserCreateSerializer(DjoserUserCreateSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    class Meta(DjoserUserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
        )
        read_only_fields = ('id', )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        slug_field = 'slug'
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id',
                                            queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Recipe.ingredients.through
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='recipe.' + ext)

        return super().to_internal_value(data)


class RecipesSerialazer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipeingredient_set'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        return (user.is_authenticated
                and Favorite.objects.filter(recipe=recipe,
                                            user=user).exists())

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        return (user.is_authenticated
                and ShoppingCart.objects.filter(recipe=recipe,
                                                user=user).exists())

    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return None


class RecipesWriteSerialazer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author',
        )
        read_only_fields = ('author',)

    def add_ingredients_to_recipe(self, recipe, ingredients_data):
        ingredients_list = []
        for ingredient_data in ingredients_data:
            ingredients_list.append(
                recipe.ingredients.through(
                    recipe=recipe,
                    ingredient=ingredient_data['ingredient']['id'],
                    amount=ingredient_data['amount']
                )
            )
        recipe.ingredients.through.objects.bulk_create(ingredients_list)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.add_ingredients_to_recipe(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.tags.set(tags_data)
        instance.ingredients.clear()
        self.add_ingredients_to_recipe(instance, ingredients_data)
        return super().update(instance, validated_data)

    def to_representation(self, recipe):
        return RecipesSerialazer(recipe, context=self.context).data


class RecipesShortSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count', )
        read_only_fields = fields

    def get_recipes(self, user):
        queryset = self.limit_recipes(user.recipes.all())
        serializer = RecipesShortSerialazer(queryset, many=True)
        return serializer.data

    def limit_recipes(self, queryset):
        limit = self.context['request'].query_params.get('recipes_limit')
        if limit:
            return queryset[:int(limit)]
        return queryset

    def get_recipes_count(self, user):
        return user.recipes.count()


class SubscribeCreateSerializer(serializers.ModelSerializer):
    subscriber = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    subscribed = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())

    class Meta:
        model = Subscribe
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=['subscriber', 'subscribed']),
        )

    def validate_subscribed(self, subscribed):
        request = self.context['request']
        if request.user == subscribed:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')
        return subscribed

    def to_representation(self, instance):
        return SubscribeSerializer(
            instance.subscribed,
            context=self.context
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe']),
        )

    def to_representation(self, instance):
        return RecipesShortSerialazer(
            instance.recipe,
            context=self.context
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Favorite
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe']),
        )

    def to_representation(self, instance):
        return RecipesShortSerialazer(
            instance.recipe,
            context=self.context
        ).data

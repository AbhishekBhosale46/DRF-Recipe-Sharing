from rest_framework import serializers
from core.models import Ingredients, Category, Recipe, InstructionSet, Step, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'qty', 'unit']
        read_only_fields = ['id']


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'step_no', 'description']
        read_only_fields = ['id']


class InstructionSetSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)

    class Meta:
        model = InstructionSet
        fields = ['id', 'prerequisite', 'steps']
        read_only_fields = ['id']

    def create(self, validated_data):
        steps_data = validated_data.pop('steps')
        instruction_set = InstructionSet.objects.create(**validated_data)
        for step_data in steps_data:
            Step.objects.create(instruction_set=instruction_set, **step_data)
        return instruction_set

    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps', None)
        instance = super().update(instance, validated_data)

        if steps_data is not None:
            existing_steps = instance.steps.all()
            for step in existing_steps:
                step.delete()
            for step_data in steps_data:
                Step.objects.create(instruction_set=instance, **step_data)
        
        return instance


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True)
    category = CategorySerializer(many=True)
    instruction_set = InstructionSetSerializer()
    created_by = serializers.SerializerMethodField('get_created_by', read_only=True)
    likes = serializers.SerializerMethodField('get_likes', read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'is_public', 'created_by', 'created_at', 'likes', 'name', 'description', 'time', 
                  'servings', 'ingredients', 'category', 'instruction_set']
        read_only_fields = ['id', 'created_by', 'created_at']

    def get_created_by(self, recipe_obj):
        created_name = recipe_obj.user.name
        return created_name

    def get_likes(self, recipe_obj):
        return recipe_obj.likes_count()

    def create(self, validated_data):
        instruction_set_data = validated_data.pop('instruction_set')
        category_data = validated_data.pop('category')
        ingredients_data = validated_data.pop('ingredients')

        instruction_set = InstructionSetSerializer(data=instruction_set_data)
        instruction_set.is_valid(raise_exception=True)
        instruction_set = instruction_set.save()

        recipe = Recipe.objects.create(instruction_set=instruction_set, **validated_data)

        for single_category_data in category_data:
            category = Category.objects.get_or_create(**single_category_data)[0]
            recipe.category.add(category)

        for ingredient_data in ingredients_data:
            ingredient = Ingredients.objects.get_or_create(**ingredient_data)[0]
            recipe.ingredients.add(ingredient)
        
        return recipe

    def update(self, instance, validated_data):
        instruction_set_data = validated_data.pop('instruction_set', None)
        category_data = validated_data.pop('category', None)
        ingredients_data = validated_data.pop('ingredients', None)

        instance = super().update(instance, validated_data)

        if instruction_set_data is not None:
            instruction_set_serializer = InstructionSetSerializer(instance.instruction_set, data=instruction_set_data)
            if instruction_set_serializer.is_valid():
                instruction_set_serializer.save()
        
        if category_data is not None:
            for single_category_data in category_data:
                category = Category.objects.get_or_create(**single_category_data)[0]
                instance.category.add(category)

        if ingredients_data is not None:
            for ingredient_data in ingredients_data:
                ingredient = Ingredients.objects.get_or_create(**ingredient_data)[0]
                instance.ingredients.add(ingredient)
        
        return instance


class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.SerializerMethodField('get_commented_by', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'commented_by', 'detail']
        read_only_fields = ['id', 'commented_by', 'created_at']

    def get_commented_by(self, comment_obj):
        name = comment_obj.user.name
        return name


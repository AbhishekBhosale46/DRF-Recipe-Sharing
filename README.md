
# Recipe Sharing Platform Api

The Recipe Sharing Platform API is a robust backend for a recipe sharing platform built using Django Rest Framework. This API enables users to share their favorite recipes, explore various groups, and discover recipes posted by others. It comes packed with features for user authentication, recipe management, ingredient tracking, and group functionality.
## Key Features

- **User Authentication:** Secure user access is ensured through token authentication, providing a safe and private environment for recipe sharing.

- **Recipe Creation:** Users can create and share their own recipes, complete with ingredients, cooking instructions, and images.

- **Group Functionality:** Explore, join, or create groups to share recipes with like-minded enthusiasts.

- **Category Exploration:** Discover recipes from various categories.

- **Ingredient-Based Exploration:** Explore recipes based on available ingredients.

- **Image Management:** Integrated Cloudinary to efficiently manage static image files within the API.


## Tech Stack

**Backend:** Django, Django RestFramework, Swagger Browsable API

**Database:** PostgreSQL

**Containerization:** Docker


## Run Locally

Clone the project

```bash
  git clone https://github.com/AbhishekBhosale46/DRF-Recipe-Sharing
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Set up the database

```bash
  python manage.py migrate
```

Start the development server

```bash
  python manage.py runserver
```




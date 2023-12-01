# IthacaTraveller-API

This was created by Frank Dai and Huajie Zhong!

# GitHub Repositories
[Ithaca Traveller - IOS](https://github.com/HackGroup1/IthacaTraveller-IOS)

[Ithaca Traveller - Backend](https://github.com/HackGroup1/IthacaTraveller-API)

# Description:

Welcome to the backend repository of Ithaca Traveler! This repository houses the server-side code and database management for our travel exploration app. The backend is designed to support the iOS and Android applications, providing a seamless and efficient experience for users.

# Ultilized libraries & Services
- Flask
- SQL
- SQLalchemy
- Docker
- Google Cloud
- Weather API


# Models

## Feature
- id
- name
- locations (many to many: one feature could have many corresponding locations)

## Location
- id
- longitude
- latitude
- name
- description
- address
- posts (one to many: one location might have many corresponding posts)
- features (many to many: one location could have many features)

## Post
- id
- timestamp
- comment
- location_id (the post belongs to one location)
- user_id (the post belongs to one user)
- liked_users (many to many: one post could be liked by many users)

## User
- id
- username
- password
- posts (one to many: one user might have many posts)
- posts_liked (many to many: one user might like many posts)


# API Specification

## Feature Routes

### Get All Features
- **Endpoint:** `/api/features/`
- **Method:** GET
- **Description:** Retrieve all features.
- **Response:** Success - List of features in JSON format.

### Get Feature by ID
- **Endpoint:** `/api/features/<int:feature_id>/`
- **Method:** GET
- **Description:** Retrieve a feature by its ID.
- **Response:** Success - Feature details in JSON format.

### Add Feature
- **Endpoint:** `/api/features/`
- **Method:** POST
- **Description:** Add a new feature.
- **Request Body:** JSON with "name" parameter.
- **Response:** Success - Empty JSON with HTTP status 201.

### Update Feature
- **Endpoint:** `/api/features/<int:feature_id>/`
- **Method:** POST
- **Description:** Update a feature by its ID.
- **Request Body:** JSON with "name" parameter.
- **Response:** Success - Empty JSON.

### Add Feature to Location
- **Endpoint:** `/api/features/<int:feature_id>/locations/<int:location_id>/`
- **Method:** POST
- **Description:** Assign a feature to a location.
- **Response:** Success - Empty JSON with HTTP status 401.

### Delete Feature by ID
- **Endpoint:** `/api/features/<int:feature_id>/`
- **Method:** DELETE
- **Description:** Delete a feature by its ID.
- **Response:** Success - Empty JSON.

## Location Routes

### Get All Locations
- **Endpoint:** `/api/locations/`
- **Method:** GET
- **Description:** Retrieve all locations.
- **Response:** Success - List of locations in JSON format.

### Get Locations ID by Feature
- **Endpoint:** `/api/locations/features/<feature>/`
- **Method:** GET
- **Description:** Retrieve location IDs associated with a feature by feature name.
- **Response:** Success - List of location IDs in JSON format.

### Get Location by ID
- **Endpoint:** `/api/locations/<int:location_id>/`
- **Method:** GET
- **Description:** Retrieve location details by its ID.
- **Response:** Success - Location details in JSON format.

### Add Location
- **Endpoint:** `/api/locations/`
- **Method:** POST
- **Description:** Add a new location.
- **Request Body:** JSON with "longitude," "latitude," "name," "address," and optional "description" parameters.
- **Response:** Success - Empty JSON with HTTP status 201.

### Update Location
- **Endpoint:** `/api/locations/<int:location_id>/`
- **Method:** POST
- **Description:** Update a location by its ID.
- **Request Body:** JSON with optional "longitude," "latitude," "name," "address" parameters.
- **Response:** Success - Empty JSON.

### Delete Location by ID
- **Endpoint:** `/api/locations/<int:location_id>/`
- **Method:** DELETE
- **Description:** Delete a location by its ID.
- **Response:** Success - Empty JSON.

## Post Routes

### Get All Posts
- **Endpoint:** `/api/posts/`
- **Method:** GET
- **Description:** Retrieve all posts.
- **Response:** Success - List of posts in JSON format.

### Get Post by ID
- **Endpoint:** `/api/posts/<int:post_id>/`
- **Method:** GET
- **Description:** Retrieve a post by its ID.
- **Response:** Success - Post details in JSON format.

### Get Posts by Location ID
- **Endpoint:** `/api/posts/locations/<int:location_id>/`
- **Method:** GET
- **Description:** Retrieve posts under a specific location by ID.
- **Query Parameters:** "sort" (optional, values: "recent" or "likes"), "user_id" (required).
- **Response:** Success - List of posts in JSON format.

### Add Post
- **Endpoint:** `/api/posts/`
- **Method:** POST
- **Description:** Add a new post.
- **Request Body:** JSON with "comment," "location_id," and "user_id" parameters.
- **Response:** Success - JSON with "post_id" and HTTP status 201.

### Update Post
- **Endpoint:** `/api/posts/<int:post_id>/`
- **Method:** POST
- **Description:** Update a post by its ID.
- **Request Body:** JSON with "comment" parameter.
- **Response:** Success - Empty JSON.

### Like Post
- **Endpoint:** `/api/posts/<int:post_id>/like/`
- **Method:** POST
- **Description:** Like or unlike a post.
- **Request Body:** JSON with "user_id" parameter.
- **Response:** Success - Empty JSON.

### Delete Post by ID
- **Endpoint:** `/api/posts/<int:post_id>/`
- **Method:** DELETE
- **Description:** Delete a post by its ID.
- **Response:** Success - Empty JSON.

## User Routes

### Get All Users
- **Endpoint:** `/api/users/`
- **Method:** GET
- **Description:** Retrieve all users.
- **Response:** Success - List of users in JSON format.

### Add User
- **Endpoint:** `/api/users/`
- **Method:** POST
- **Description:** Add a new user.
- **Request Body:** JSON with "username" and "password" parameters.
- **Response:** Success - JSON with "user_id" and HTTP status 201.

### Get User by ID
- **Endpoint:** `/api/users/<int:user_id>/`
- **Method:** GET
- **Description:** Retrieve a user by its ID.
- **Response:** Success - User details in JSON format.

### Delete User by ID
- **Endpoint:** `/api/users/<int:user_id>/`
- **Method:** DELETE
- **Description:** Delete a user by its ID.
- **Response:** Success - Empty JSON.

### Verify User
- **Endpoint:** `/api/users/verify/`
- **Method:** POST
- **Description:** Verify user credentials.
- **Request Body:** JSON with "username" and "password" parameters.
- **Response:** Success - JSON with "verify" (True/False) and "user_id" (if verified).

## Image Routes

### Get Post Image by Post ID
- **Endpoint:** `/api/images/posts/<int:post_id>/`
- **Method:** GET
- **Description:** Retrieve a post image by its post ID.
- **Response:** Image file.

### Get User Profile Image by User ID
- **Endpoint:** `/api/images/user/<int:user_id>/`
- **Method:** GET
- **Description:** Retrieve a user profile image by its user ID.
- **Response:** Image file.

### Post Post Image by Post ID
- **Endpoint:** `/api/images/posts/<int:post_id>/`
- **Method:** POST
- **Description:** Upload a post image by its post ID.
- **Response:** Success - Empty JSON.

### Post User Profile Image by User ID
- **Endpoint:** `/api/images/user/<int:user_id>/`
- **Method:** POST
- **Description:** Upload a user profile image by its user ID.
- **Response:** Success - Empty JSON.

### Delete Post Image by Post ID
- **Endpoint:** `/api/images/post/<int:post_id>/`
- **Method:** DELETE
- **Description:** Delete a post image by its post ID.
- **Response:** Success - Empty JSON.

### Delete User Profile Image by User ID
- **Endpoint:** `/api/images/user/<int:user_id>/`
- **Method:** DELETE
- **Description:** Delete a user profile image by its user ID.
- **Response:** Success - Empty JSON.

## Weather Route

### Get Weather at Given Position
- **Endpoint:** `/api/weather/`
- **Method:** GET
- **Description:** Obtain weather information at the given position.
- **Query Parameters:** "longitude" and "latitude" (sent as arguments).
- **Response:** Weather information in the format specified by the frontend.

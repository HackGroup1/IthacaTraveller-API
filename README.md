# IthacaTraveller-API

This was created by Frank Dai and Huajie Zhong!

Link to the [front end IOS repo](https://github.com/HackGroup1/IthacaTraveller-IOS):

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


# API Specifications

## Feature Routes

### GET all features
- Endpoint: `/api/features/`
- Returns: List of all features.

### GET feature by id
- Endpoint: `/api/features/<int:feature_id>/`
- Returns: Feature details based on the provided feature_id.

### POST feature (create feature)
- Endpoint: `/api/features/`
- Payload: JSON body with a "name" parameter.
- Returns: Empty response with status code 201 if successful.

### POST feature by id (update feature)
- Endpoint: `/api/features/<int:feature_id>/`
- Payload: JSON body with a "name" parameter.
- Returns: Empty response with status code 200 if successful.

### POST feature by location_id (assign feature to location)
- Endpoint: `/api/features/<int:feature_id>/locations/<int:location_id>/`
- Returns: Empty response with status code 401 if successful.

### DELETE feature by id
- Endpoint: `/api/features/<int:feature_id>/`
- Returns: Empty response with status code 200 if successful.

## Location Routes

### GET all locations
- Endpoint: `/api/locations/`
- Returns: List of all locations.

### GET locations’ id by feature
- Endpoint: `/api/locations/features/<feature>/`
- Returns: List of location IDs associated with the provided feature.

### GET location by id
- Endpoint: `/api/locations/<int:location_id>/`
- Returns: Location details based on the provided location_id.

### POST location (create location)
- Endpoint: `/api/locations/`
- Payload: JSON body with "longitude," "latitude," "name," and "address" parameters.
- Returns: Empty response with status code 201 if successful.

### POST location by id (update location)
- Endpoint: `/api/locations/<int:location_id>/`
- Payload: JSON body with optional "longitude," "latitude," "name," and "address" parameters.
- Returns: Empty response with status code 200 if successful.

### DELETE location by id
- Endpoint: `/api/locations/<int:location_id>/`
- Returns: Empty response with status code 200 if successful.

## Post Routes

### GET all posts
- Endpoint: `/api/posts/`
- Returns: List of all posts.

### GET post by id
- Endpoint: `/api/posts/<int:post_id>/`
- Returns: Post details based on the provided post_id.

### GET posts by location_id
- Endpoint: `/api/posts/locations/<int:location_id>/`
- Query Parameters: "user_id" (required), "sort" (optional, values: "recent" or "likes").
- Returns: List of posts under a specific location, sorted based on the provided criteria.

### POST post (create post)
- Endpoint: `/api/posts/`
- Payload: JSON body with "comment," "location_id," and "user_id" parameters.
- Returns: JSON response with the new post_id and status code 201 if successful.

### POST post by id (update post)
- Endpoint: `/api/posts/<int:post_id>/`
- Payload: JSON body with a "comment" parameter.
- Returns: Empty response with status code 200 if successful.

### POST like post
- Endpoint: `/api/posts/<int:post_id>/like/`
- Payload: JSON body with a "user_id" parameter.
- Returns: Empty response with status code 200 if successful.

### DELETE post by id
- Endpoint: `/api/posts/<int:post_id>/`
- Returns: Empty response with status code 200 if successful.

## User Routes

### GET all users
- Endpoint: `/api/users/`
- Returns: List of all users.

### POST user (create user)
- Endpoint: `/api/users/`
- Payload: JSON body with "username" and "password" parameters.
- Returns: Empty response with status code 201 if successful.

### GET user by id
- Endpoint: `/api/users/<int:user_id>/`
- Returns: User details based on the provided user_id.

### DELETE user by id
- Endpoint: `/api/users/<int:user_id>/`
- Returns: Empty response with status code 200 if successful.

### POST verify user password and username
- Endpoint: `/api/users/verify/`
- Payload: JSON body with "username" and "password" parameters.
- Returns: JSON response indicating whether the password is correct along with the user_id.

## Extra Routes

### Images
#### GET post image by post_id
- Endpoint: `/api/images/posts/<int:post_id>/`
- Returns: Image file associated with the post_id.

#### GET user profile image by user_id
- Endpoint: `/api/images/user/<int:user_id>/`
- Returns: Image file associated with the user_id.

#### POST post image by post_id
- Endpoint: `/api/images/posts/<int:post_id>/`
- Returns: Empty response with status code 200 if successful.

#### POST user profile image by user_id
- Endpoint: `/api/images/user/<int:user_id>/`
- Returns: Empty response with status code 200 if successful.

#### DELETE post image by post_id
- Endpoint: `/api/images/post/<int:post_id>/`
- Returns: Empty response with status code 200 if successful.

#### DELETE user profile image by user_id
- Endpoint: `/api/images/user/<int:user_id>/`
- Returns: Empty response with status code 200 if successful.

### Weather
#### GET weather at the given position
- Endpoint: `/api/weather/`
- Payload: JSON body with "longitude" and "latitude" parameters.
- Returns: Weather information in the format specified by the front end.

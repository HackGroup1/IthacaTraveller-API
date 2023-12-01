# IthacaTraveller-API

This was created by Frank Dai and Huajie Zhong!

Link to the front end IOS repo: https://github.com/HackGroup1/IthacaTraveller-IOS

# Description:

Welcome to the backend repository of Ithaca Traveler! This repository houses the server-side code and database management for our travel exploration app. The backend is designed to support the iOS and Android applications, providing a seamless and efficient experience for users.

# Ultilized libraries & Services
- Flask
- SQL
- SQLalchemy
- Docker
- Google Cloud
- Weather API

# API Specification
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

# APIs

## Feature
- GET all features
  - /api/features/
- GET feature by id
  - /api/features/<int:feature_id>/
- POST feature (create feature)
  - /api/features/
- POST feature by id (update feature)
  - /api/features/<int:feature_id>/
- POST feature by location_id (assign feature to location)
  - /api/features/<int:feature_id>/locations/<int:location_id>/
- DELETE feature by id
  - /api/features/<int:feature_id>/

## Location
- GET all locations
  - /api/locations/
- GET location by id
  - /api/locations/<int:location_id>/
- GET locations’ id by feature
  - /api/locations/features/<feature>/
- POST location (create location)
  - /api/locations/
- POST location by id (update location)
  - /api/locations/<int:location_id>/
- DELETE location by id
  - /api/locations/<int:location_id>/

## Post
- GET all posts
  - /api/posts/
- GET post by id
  - /api/locations/<int:location_id>/
- GET posts by location_id (requires user_id to check which posts are editable) takes in parameter sort to return in order by most like or recent
  - /api/posts/locations/<int:location_id>/
  - /api/posts/locations/<int:location_id>?sorted_by=recent
- POST post (create post, requires its location and owner/user)
  - /api/posts/
- POST post by location_id and user_id (edit post, requires)
- DELETE post by id
  - /api/posts/<int:post_id>/
- POST like post
  - /api/posts/<int:post_id>/like/

## User
- GET all users
  - /api/users/
- GET user by id
  - /api/users/<int:user_id>/
- GET verify user password and username
  - /api/users/verify/
- POST user (create user, requires password)
  - /api/users/
- POST user by id (update user info, requires password)
- DELETE user by id
  - /api/users/<int:user_id>/

# Extra things

## Images
We store images in server directories.
We have two kinds of images: 
- User profile images (stored under ~/images/users/)
- Post images (stored under ~/images/posts/)
We restrict each post to have at most one image, and restrict each user to have exactly one profile image. In this way, we can use user_id to name the user profile images and use post_id to name the post images.

### Corresponding APIs:
- GET post image by post_id
  - /api/images/posts/<int:post_id>/
- GET user profile image by user_id
  - /api/images/user/<int:user_id>/
- POST post image by post_id
  - /api/images/posts/<int:post_id>/
- POST user profile image by user_id
  - /api/images/user/<int:user_id>/
- DELETE post image by post_id
  - /api/images/post/<int:post_id>/
- DELETE user profile image by user_id
  - /api/images/user/<int:user_id>/

## Weather
Obtain weather information using API by weatherapi.com
Returns in the format specified by the front end

- GET weather at the given position (requires longitude and latitude (sent as JSON))
  - /api/weather/

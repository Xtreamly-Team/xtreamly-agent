# Xtreamly

This project holds the Xtreamly UI.

# Prerequisites

1. Nvm installed on the machine, or Node version v20.18.0 (inside the .nvmrc file)

## Local setup

### Install requirements

1. Clone repo
2. Use correct node version in `.nvmrc` or run `nvm use`
3. Install yarn: `npm install -g yarn`
4. Install libraries: `yarn`

### Start the Application

`yarn start`

Or you can run the UI and Backend separately:

1. Start the backend: `yarn start:backend`
2. Start the frontend: `yarn start:ui`

### Accessing the application

You access the different parts of the APP:

1. UI: http://localhost:5173/
2. APIs: http://127.0.0.1:5001/devote-ba3e8/us-central1
3. Firebase Emulators: http://127.0.0.1:4000/

## Deploy

This project is using CI/CD pipelines to deploy on Firebase cloud.
Every merge on the main branch will automatically deploy the application into firebase.

### Backend

1. `cd backend`
2. `yarn deploy`

### Frontend

1. `nvm use`
2. `firebase deploy --only hosting`
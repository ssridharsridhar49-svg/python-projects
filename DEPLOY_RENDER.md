# Render deployment

The repository includes a Render Blueprint (`render.yaml`) for a Django web service and PostgreSQL database. It uses WhiteNoise for static assets, runs migrations and `collectstatic` during each build, and generates the Django secret in Render rather than storing it in this repository.

## Deploy

1. Push this repository to GitHub.
2. In Render, create a **Blueprint** and connect the GitHub repository.
3. Apply the Blueprint. It creates the `autocraft-sridhar459` web service and its PostgreSQL database.
4. Wait for the first deploy to finish, then open `https://autocraft-sridhar459.onrender.com/`.

The database starts empty. The Django migration seeds the sample vehicle catalog. The local SQLite database is intentionally excluded because it contains account, saved-design, and contact-message records.

## Free plan notes

The Blueprint uses Render's free web and PostgreSQL plans. Free web services can spin down when idle, and their filesystem is temporary; uploaded media files are not durable. Render's free PostgreSQL databases expire 30 days after creation. Upgrade the database before its expiry to keep it and its data. Check Render's current plan details before upgrading.

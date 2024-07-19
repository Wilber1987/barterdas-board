{
  "dev": {
    "django_settings": "bcapital.settings.dev",
    "profile_name": "barter",
    "project_name": "dashboard-api",
    "runtime": "python3.9",
    "s3_bucket": "dashboard-backend-apiv2",
    "serve_async": false,
    "aws_region": "us-east-1",
    "extra_permissions": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ],
        "Resource": [
          "arn:aws:s3:::dashboard-backend-apiv2",
          "arn:aws:s3:::dashboard-backend-apiv2/*"
        ]
      }
    ],
    "aws_environment_variables": {
      "APP_KEY": "$APP_KEY",
      "APP_DEBUG": "True",
      "DB_NAME_PROD": "$DB_NAME_PROD",
      "DB_HOST_PROD": "$DB_HOST_PROD",
      "DB_USER_PROD": "$DB_USER_PROD",
      "DB_PASSWORD_PROD": "$DB_PASSWORD_PROD",
      "DB_PORT": "$DB_PORT",
      "DB_NAME_DEV": "$DB_NAME_DEV",
      "DB_HOST_DEV": "$DB_HOST_DEV",
      "DB_USER_DEV": "$DB_USER_DEV",
      "DB_PASSWORD_DEV": "$DB_PASSWORD_DEV",
      "DB_NAME_STAGING": "$DB_NAME_STAGING",
      "DB_HOST_STAGING": "$DB_HOST_STAGING",
      "DB_USER_STAGING": "$DB_USER_STAGING",
      "DB_PASSWORD_STAGING": "$DB_PASSWORD_STAGING",
      "AWS_SES_ACCESS_KEY_ID": "$AWS_SES_ACCESS_KEY_ID",
      "AWS_SES_SECRET_ACCESS_KEY": "$AWS_SES_SECRET_ACCESS_KEY",
      "AWS_SMTP_USER": "$AWS_SMTP_USER",
      "AWS_SMTP_PASSWORD": "$AWS_SMTP_PASSWORD",
      "FRONTEND_URL_DEV": "$FRONTEND_URL_DEV",
      "FRONTEND_URL_PROD": "$FRONTEND_URL_PROD",
      "SENDER_EMAIL": "$SENDER_EMAIL",
      "SUPPORT_EMAIL": "$SUPPORT_EMAIL",
      "ROLLBAR_ACCESS_TOKEN": "$ROLLBAR_ACCESS_TOKEN",
      "DJANGO_SETTINGS_MODULE": "bcapital.settings.dev",
      "REQUEST_TIMEOUT": "$REQUEST_TIMEOUT",
      "SUMSUB_BASE_URL": "$SUMSUB_BASE_URL",
      "SUMSUB_APP_TOKEN": "$SUMSUB_APP_TOKEN",
      "SUMSUB_SECRET_KEY": "$SUMSUB_SECRET_KEY",
    },
    "tags": {
      "Project": "dashboard-api",
      "Environment": "dev",
      "Owner": "devops"
    }
  },
  "staging": {
    "django_settings": "bcapital.settings.staging",
    "profile_name": "barter",
    "project_name": "dashboard-api-staging",
    "runtime": "python3.9",
    "s3_bucket": "dashboard-backend-apiv2-staging",
    "serve_async": false,
    "aws_region": "us-east-1",
    "extra_permissions": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ],
        "Resource": [
          "arn:aws:s3:::dashboard-backend-apiv2-staging",
          "arn:aws:s3:::dashboard-backend-apiv2-staging/*"
        ]
      }
    ],
    "aws_environment_variables": {
      "APP_KEY": "$APP_KEY",
      "APP_DEBUG": "True",
      "DB_NAME_PROD": "$DB_NAME_PROD",
      "DB_HOST_PROD": "$DB_HOST_PROD",
      "DB_USER_PROD": "$DB_USER_PROD",
      "DB_PASSWORD_PROD": "$DB_PASSWORD_PROD",
      "DB_PORT": "$DB_PORT",
      "DB_NAME_DEV": "$DB_NAME_DEV",
      "DB_HOST_DEV": "$DB_HOST_DEV",
      "DB_USER_DEV": "$DB_USER_DEV",
      "DB_PASSWORD_DEV": "$DB_PASSWORD_DEV",
      "DB_NAME_STAGING": "$DB_NAME_STAGING",
      "DB_HOST_STAGING": "$DB_HOST_STAGING",
      "DB_USER_STAGING": "$DB_USER_STAGING",
      "DB_PASSWORD_STAGING": "$DB_PASSWORD_STAGING",
      "AWS_SES_ACCESS_KEY_ID": "$AWS_SES_ACCESS_KEY_ID",
      "AWS_SES_SECRET_ACCESS_KEY": "$AWS_SES_SECRET_ACCESS_KEY",
      "AWS_SMTP_USER": "$AWS_SMTP_USER",
      "AWS_SMTP_PASSWORD": "$AWS_SMTP_PASSWORD",
      "FRONTEND_URL_DEV": "$FRONTEND_URL_STAGING",
      "FRONTEND_URL_PROD": "$FRONTEND_URL_PROD",
      "SENDER_EMAIL": "$SENDER_EMAIL",
      "SUPPORT_EMAIL": "$SUPPORT_EMAIL",
      "ROLLBAR_ACCESS_TOKEN": "$ROLLBAR_ACCESS_TOKEN",
      "DJANGO_SETTINGS_MODULE": "bcapital.settings.staging",
      "REQUEST_TIMEOUT": "$REQUEST_TIMEOUT",
      "SUMSUB_BASE_URL": "$SUMSUB_BASE_URL",
      "SUMSUB_APP_TOKEN": "$SUMSUB_APP_TOKEN",
      "SUMSUB_SECRET_KEY": "$SUMSUB_SECRET_KEY",
    },
    "tags": {
      "Project": "dashboard-api",
      "Environment": "staging",
      "Owner": "devops"
    }
  },
  "prod": {
    "django_settings": "bcapital.settings.prod",
    "profile_name": "barter",
    "project_name": "dashboard-api-prod",
    "runtime": "python3.9",
    "s3_bucket": "dashboard-backend-apiv2-prod",
    "aws_region": "us-east-1",
    "domain": "api.bartercapital-dashboard.com",
    "certificate_arn": "arn:aws:acm:us-east-1:489076568171:certificate/d8f547c3-be87-47dc-b7b1-f3d3a112b36a",
    "extra_permissions": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ],
        "Resource": [
          "arn:aws:s3:::dashboard-backend-apiv2-prod",
          "arn:aws:s3:::dashboard-backend-apiv2-prod/*"
        ]
      }
    ],
    "aws_environment_variables": {
      "APP_KEY": "$APP_KEY",
      "APP_DEBUG": "False",
      "DB_NAME_PROD": "$DB_NAME_PROD",
      "DB_HOST_PROD": "$DB_HOST_PROD",
      "DB_USER_PROD": "$DB_USER_PROD",
      "DB_PASSWORD_PROD": "$DB_PASSWORD_PROD",
      "DB_PORT": "$DB_PORT",
      "DB_NAME_DEV": "$DB_NAME_DEV",
      "DB_HOST_DEV": "$DB_HOST_DEV",
      "DB_USER_DEV": "$DB_USER_DEV",
      "DB_PASSWORD_DEV": "$DB_PASSWORD_DEV",
      "DB_NAME_STAGING": "$DB_NAME_STAGING",
      "DB_HOST_STAGING": "$DB_HOST_STAGING",
      "DB_USER_STAGING": "$DB_USER_STAGING",
      "DB_PASSWORD_STAGING": "$DB_PASSWORD_STAGING",
      "AWS_SES_ACCESS_KEY_ID": "$AWS_SES_ACCESS_KEY_ID",
      "AWS_SES_SECRET_ACCESS_KEY": "$AWS_SES_SECRET_ACCESS_KEY",
      "AWS_SMTP_USER": "$AWS_SMTP_USER",
      "AWS_SMTP_PASSWORD": "$AWS_SMTP_PASSWORD",
      "FRONTEND_URL_DEV": "$FRONTEND_URL_DEV",
      "FRONTEND_URL_PROD": "$FRONTEND_URL_PROD",
      "SENDER_EMAIL": "$SENDER_EMAIL",
      "SUPPORT_EMAIL": "$SUPPORT_EMAIL",
      "ROLLBAR_ACCESS_TOKEN": "$ROLLBAR_ACCESS_TOKEN",
      "DJANGO_SETTINGS_MODULE": "bcapital.settings.prod",
      "REQUEST_TIMEOUT": "$REQUEST_TIMEOUT",
      "SUMSUB_BASE_URL": "$SUMSUB_BASE_URL",
      "SUMSUB_APP_TOKEN": "$SUMSUB_APP_TOKEN",
      "SUMSUB_SECRET_KEY": "$SUMSUB_SECRET_KEY",
      "SUMSUB_PROD_APP_TOKEN": "$SUMSUB_PROD_APP_TOKEN",
      "SUMSUB_PROD_SECRET_KEY": "$SUMSUB_PROD_SECRET_KEY",
    },
    "tags": {
      "Project": "dashboard-api",
      "Environment": "prod",
      "Owner": "devops"
    }
  }
}

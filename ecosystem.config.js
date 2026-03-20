module.exports = {
  apps: [
    {
      name: "aisetu_erp",
      script: "gunicorn",
      args: "-c gunicorn_config.py aisetu_erp.wsgi:application",
      cwd: "./aisetu_erp",
      interpreter: "python", // Assuming python is in PATH or using venv
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      env: {
        NODE_ENV: "production",
        DJANGO_DEBUG: "False",
        DJANGO_ALLOWED_HOSTS: "*", // Replace with your domain
      },
      error_file: "../pm2_error.log",
      out_file: "../pm2_out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss",
    },
  ],
};

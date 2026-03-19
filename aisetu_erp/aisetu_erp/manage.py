import os
import sys

def apply_mongodb_bulk_create_patch():
    """
    Monkeypatch Django's bulk_create to populate ObjectIds back to the model 
    instances, fixing the 'unhashable TypeError' during post_migrate.
    """
    try:
        from django.db.models.query import QuerySet
        original_bulk_create = QuerySet.bulk_create
        
        def patched_bulk_create(self, objs, batch_size=None, ignore_conflicts=False, update_conflicts=False, update_fields=None, unique_fields=None):
            # Let Django do the insert
            returned_objs = original_bulk_create(
                self, objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts, 
                update_conflicts=update_conflicts, update_fields=update_fields, unique_fields=unique_fields
            )
            
            # Temporary fix for django-mongodb-backend: bulk_create doesn't set PKs
            # We fetch them back from the DB based on the fields if the PK is missing.
            from django.conf import settings
            if settings.DATABASES['default']['ENGINE'] == 'django_mongodb_backend':
                pk_field = self.model._meta.pk.attname
                for obj in returned_objs:
                    if getattr(obj, pk_field, None) is None:
                        # For ContentType, we can lookup by app_label and model
                        if self.model.__name__ == 'ContentType':
                            db_obj = self.model.objects.filter(app_label=obj.app_label, model=obj.model).first()
                            if db_obj:
                                setattr(obj, pk_field, getattr(db_obj, pk_field))
                        # For Permission, lookup by content_type and codename
                        elif self.model.__name__ == 'Permission':
                            db_obj = self.model.objects.filter(content_type=obj.content_type, codename=obj.codename).first()
                            if db_obj:
                                setattr(obj, pk_field, getattr(db_obj, pk_field))
            return returned_objs
        
        QuerySet.bulk_create = patched_bulk_create
    except ImportError:
        pass

def run_frontend_build():
    """
    Runs the React frontend build command (npm run build).
    """
    import subprocess
    from pathlib import Path
    
    # Define paths
    base_dir = Path(__file__).resolve().parent
    # The nested manage.py is in aisetu_erp/aisetu_erp/
    # Frontend is in ../../Frontend
    frontend_dir = base_dir.parent.parent / 'Frontend' / 'landing-page-launchpad-main'
    
    if not frontend_dir.exists():
        print(f"Warning: Frontend directory not found at {frontend_dir}")
        return

    print(f"Building frontend in {frontend_dir}...")
    try:
        # Check if node_modules exists, if not run npm install
        if not (frontend_dir / 'node_modules').exists():
            print("node_modules not found. Running 'npm install'...")
            # Use default stdout/stderr so output is visible in real-time
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True, shell=True)
            
        # Run build
        print("Running 'npm run build'...")
        subprocess.run(['npm', 'run', 'build'], cwd=frontend_dir, check=True, shell=True)
        print("Frontend build successful.")
    except subprocess.CalledProcessError as e:
        print(f"--- ERROR: Frontend build failed (exit code {e.returncode}) ---")
        print("------------------------------------------------------")
    except Exception as e:
        print(f"An unexpected error occurred during frontend build: {e}")

def main():
    """Run administrative tasks."""
    print("--- DEBUG: manage.py starting ---")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aisetu_erp.settings')
    
    # --- AUTOMATED FRONTEND BUILD ---
    # Run build for commands that need it (runserver, collectstatic)
    if len(sys.argv) > 1 and sys.argv[1] in ['runserver', 'collectstatic']:
        # Removing RUN_MAIN check for now to ensure this triggers on the server
        run_frontend_build()
    # --------------------------------
    
    try:
        from django.core.management import execute_from_command_line
        
        # --- MONGO DB MIGRATION FIX ---
        # Disconnect the auth post_migrate signal which crashes on mongodb 
        # (due to bulk_create not returning PKs for the Permission models)
        if len(sys.argv) > 1 and sys.argv[1] == 'migrate':
            try:
                from django.db.models.signals import post_migrate
                from django.contrib.auth.management import create_permissions
                post_migrate.disconnect(
                    receiver=create_permissions,
                    dispatch_uid="django.contrib.auth.management.create_permissions"
                )
                print("Note: Disabled auth.create_permissions post_migrate signal for MongoDB compatibility.")
            except Exception:
                pass
        # ------------------------------
        
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Robustly set default port for runserver if not provided
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        if len(sys.argv) == 2 or sys.argv[2].startswith('--'):
            sys.argv.insert(2, '0.0.0.0:5004')
            print(f"Note: Automatically using default address 0.0.0.0:5004")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

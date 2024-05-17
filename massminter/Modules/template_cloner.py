import os
import shutil

def clone_minter_folder():
    # Define the paths
    main_directory = os.path.expanduser("~/Desktop/mass minter")
    template_folder = os.path.join(main_directory, "minter")
    cloned_minters_directory = os.path.join(main_directory, "cloned minters")
    env_file_path = os.path.join(main_directory, ".env")
    
    # Ensure the cloned minters directory exists
    os.makedirs(cloned_minters_directory, exist_ok=True)
    
    # Prompt the user for the number of instances
    while True:
        try:
            num_instances = int(input("How many instances? "))
            if num_instances <= 0:
                raise ValueError("Number of instances must be a positive integer.")
            break
        except ValueError as e:
            print(e)
    
    # Clone the template folder and copy the .env file
    for i in range(num_instances):
        instance_folder = os.path.join(cloned_minters_directory, f"minter_instance_{i+1}")
        shutil.copytree(template_folder, instance_folder)
        shutil.copy(env_file_path, instance_folder)
        print(f"Cloned minter to {instance_folder} and copied .env file.")

    print("Cloning completed successfully.")

# Run the clone function
if __name__ == "__main__":
    clone_minter_folder()

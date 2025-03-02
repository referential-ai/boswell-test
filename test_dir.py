import os
import time

# Function to create a directory with a free tag
def create_dir_with_free_tag(domain_name, is_free=False):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    free_tag = "-free" if is_free else ""
    run_dir = f"results/{timestamp}-{domain_name}{free_tag}"
    
    if not os.path.exists("results"):
        os.makedirs("results")
        
    os.makedirs(run_dir, exist_ok=True)
    print(f"Created directory: {run_dir}")
    return run_dir

# Test with free tag
dir_with_free = create_dir_with_free_tag("test_domain", is_free=True)
# Test without free tag
dir_without_free = create_dir_with_free_tag("test_domain", is_free=False)

print(f"Directory with free tag: {dir_with_free}")
print(f"Directory without free tag: {dir_without_free}")

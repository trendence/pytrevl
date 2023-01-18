# This file is run inside the jupyter-lab container to set-up the
# See: https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#startup-hooks

set -e
set -x
echo "Running PyTrevl jupyter-lab setup..."

# Install runtime dependencies
pip install "CubeJsClient>=0.1.1,<0.2"

# Install dev dependencies
conda install "pytest>=7.2,<8"

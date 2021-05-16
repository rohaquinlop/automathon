source ./virtualEnv.sh
route= "dist/${1}"
python -m twine upload "$route"
deactivate

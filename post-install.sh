# Regenerate requirements.txt
echo "Regenerating requirements.txt..."
pipenv run pipenv_to_requirements -f


# Clear pipenv caches
echo "Clearing pipenv caches..."
pipenv --clear

echo "Done!"

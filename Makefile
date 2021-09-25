help:
	@echo "Disease spread simulation with cellular automaton"
	@echo ""
	@echo "COMMANDS"
	@echo "    help: application help"
	@echo "    compile: create executable"

compile:
	pip install -r ./requirements.txt
	pyinstaller -F ./simulation/__main__.py -n dss --hidden-import dotenv --clean -i ./icon.ico
	chmod +x dist/dss
	cat ./simulation.config > dist/simulation.config
*The very first line must be italicized and read: This project has been created as part
of the 42 curriculum by sgarba, edraheim.*

# A-MAZE-ING-42

## Description
This is the "A-MAZE-ING" project from the 42 school.
The goal was to create a reuseable maze generator module and to wirte a program
that reads the configuration data from the cofig.txt file and creates a maze with the
maze generator module.
AMAZING is the root directory of the Project.
It contains: 
- the mazegen module in the mazegen directory
- the a_maze_ing.py file which contains the script to run the program
- the config.txt file where the maze configuration data is stored
- the LICENSE.md which contains the MIT licencse
- the pyproject.toml file to manage the packages
- the README.md which contains the documents
- the Makefile which contains the commands to run the program



## Instructions

If you want to intall the maze generator module in your project you have to add the mazegen module to your root directory first. Then run following the command to build the package
```bash 
            pip install build --break-system-packages
            python3 -m build
```
This will create the directoary \dist with the files:
- dist/mazegen_eric-1.0.0-py3-none-any.whl
- dist/mazegen_eric-1.0.0.tar.gz

Now you can install the package in your project with the command:

```bash 
        pip install dist/mazegen_eric-1.0.0-py3-none-any.whl    
```
and import it to your files with:
```bash 
        from mazgen import MazeGenerator
```
Now you are ready to create new instances of the maze generator:

```bash   
        maze = MazeGenerator(10, 10)
        maze.generate()
```

To run the program run use the command:
```bash   
    make run
```
To run the programm in the perfect mode use the command
```bash   
    make run $ARGS='--perfect'
```
• The complete structure and format of your config file.
# config.txt structre
The config .txt file contains the configuration data of the maze. The data is stored in KEY=VALUE pairs as strings.
```bash
    WIDTH=20
    HEIGHT=15
    ENTRY=1,2
    EXIT=12,10
    OUTPUT_FILE=maze.txt
    PERFECT=False
```
## Agorithm - DFS
We have used the DFS (depth-first-search) algorithm to create the maze. The idea of DFS is that the Algo goes always in one direction until it has to stop for example it hits the 42-cell or a border then it goes back until it finds the last valid cell from wehre it can go in another direction until it has to stop and then it repeats the process until  all cells are visited. We have chosen this the DFS algorithm because it is perfect to create "--perfect" mazes.




• What part of your code is reusable, and how.
• Your team and project management with:
◦ The roles of each team member.
◦ Your anticipated planning and how it evolved until the end
◦ What worked well and what could be improved
◦ Have you used any specific tools? Which ones?
If you implement advanced features (multiple algorithms, display options), describe them
in this README.md file.
## Resources
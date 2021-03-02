# BWPlanner

BWPlanner is a domain specific planner for the [blocks world](https://en.wikipedia.org/wiki/Blocks_world) domain written for learning purposes.

It consists of a bounded suboptimal solver and an A\* solver with a domain specific heuristic. Both can be combined in a simple form of anytime search.

It does not implement a full PDDL parser. Problems must adhere to [this](http://www.plg.inf.uc3m.es/ipc2011-learning/attachments/Domains/blocksworld.pddl) domain definition published by the [\[plg\]](http://www.plg.inf.uc3m.es) research group.

## Dependencies

BWPlanner requires [Python](https://www.python.org/) version 3.8 or later.

## Running the planner

Find an optimal plan for the given problem:
```
./bwplanner.py -o problems/pfile10.pddl
```

Find a valid plan for the given problem:
```
./bwplanner.py -n problems/pfile30.pddl
```

Find a valid plan for the given problem and then try to find an optimal plan until the program is interrupted:
```
./bwplanner.py -n -o problems/pfile16.pddl
```

## Screenshot

![screenshot](https://raw.githubusercontent.com/nramon/BWPlanner/main/doc/bwplanner.png)

## Copyright

Copyright (C) 2021 Ramon Novoa ramonnovoa@gmail.com

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

# CrossoutML
 
conda activate crossoutML
python main.py


# To Buy
Grenadier
Cheetah
Hot Red
MD-3 Owl
Gasgen
Grinder


### Add Chemical Plant Map


## Init Protobuf database
.\protoc.exe -I="C:\Users\gaming\Documents\GitHub\CrossoutML" --python_out="C:\Users\gaming\Documents\GitHub\CrossoutML" C:\Users\gaming\Documents\GitHub\CrossoutML\crossml.proto


## Movement Principle

set a recording delay frame count

when detected that 1 side of the car is outside of allowed zone

set init too close to the side of outside

then start press turn keys, a or d

to make sure it turns only along th edge not 180 backwards, the turn should stop when the front detection is in allowed zone, so that the car is parallel (kind of) to the edge of allowed zone.

However because of the delay, the car will receive the information a little too late.

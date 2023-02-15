.PHONY: clean

mockRobot: clean
	grep -v "BP" robot.py | grep -v "brickpi3" >> mockRobot.py

clean:
	cp mockRobot_doc.txt mockRobot.py

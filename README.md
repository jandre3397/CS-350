# CS-350

### Project Summary and Reflection

This project focused on developing a functional thermostat prototype using a Raspberry Pi 4 and various connected peripherals. The goal was to build a low-level system that could monitor room temperature, allow users to switch between heating, cooling, and off modes, and provide clear visual feedback through LEDs, a 16x2 LCD display, and UART serial output. The thermostat used a SHT41 sensor to read environmental conditions and implemented a state machine in Python to manage system behavior based on user input.

One thing I did particularly well was structuring the codebase to be highly organized and modular. Breaking the project into manageable classes, such as the state machine (`TemperatureMachine`) and display management (`ManagedDisplay`), made the system easier to develop, debug, and later extend. I also successfully adapted when encountering hardware challenges—such as replacing the original AHT20 sensor with an SHT41—and quickly modified the software without breaking functionality.

An area I could improve is initial testing of user interface elements. Although the final version worked smoothly, earlier and more focused testing of the button responsiveness and LED transitions could have sped up development and reduced rework later on.

During the project, I expanded my tools and resources significantly. I gained experience with CircuitPython sensor libraries, the gpiozero package for managing GPIO devices, the serial library for UART communication, and draw.io for visualizing system states. These tools will continue to support my development work in embedded systems and IoT projects.

Key skills I developed that are transferable to other coursework and projects include designing state machines, managing GPIO and I2C communication, implementing real-time user feedback loops, and ensuring clean, modular code organization. These experiences will be highly valuable in future embedded projects, cloud integration tasks, and system design work.

I made the project maintainable, readable, and adaptable by using consistent code formatting, clear naming conventions, detailed inline comments, and class-based modular design. By isolating the hardware interaction logic from the core thermostat behavior, the system can easily be adapted in the future to support new sensors, cloud connectivity, or expanded functionality without requiring a full rewrite.


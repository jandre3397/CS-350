# CS-350


# Project Reflection 

This project focused on designing and prototyping a smart thermostat system to help SysTec enter the growing smart home market. The main problem we aimed to solve was building a low-level, embedded system capable of monitoring environmental conditions, responding to user input, managing system state transitions (off, heat, cool), and preparing for future cloud connectivity. I successfully integrated real-world hardware components—including a SHT41 temperature and humidity sensor, PWM LED indicators, UART serial communication, button interfaces, and a 16x2 LCD—into a cohesive, functional prototype.

One thing I did particularly well was designing and implementing the state machine architecture that governed thermostat behavior. Carefully defining clear states, managing transitions reliably, and reflecting those changes instantly through visual (LEDs, LCD) and backend (UART) outputs created a strong foundation for a future production system. I was also able to adapt when challenges arose, such as replacing the temperature sensor hardware and quickly updating the codebase to support the new device while maintaining functionality.

If I were to improve anything, it would be earlier testing and refinement of the user interface responsiveness—particularly making the LCD updates smoother when setpoints changed. While I successfully caught and solved these details during later testing, building in rapid user feedback earlier would have made the user experience even stronger.

Throughout this project, I expanded my support network and toolkit by diving deeper into Raspberry Pi configuration, embedded Linux, GPIO libraries like gpiozero, and sensor libraries such as Adafruit’s CircuitPython support. I also began using draw.io more effectively for designing maintainable system diagrams like the state machine, which will be valuable for communicating architecture in future projects.

Several skills from this project are highly transferable: designing state machines, integrating real-time sensor feedback, managing hardware interfaces (I2C, UART, PWM), and structuring software in modular, readable ways. These abilities are critical not only for future embedded systems projects but also for larger coursework involving IoT, networking, or cloud-based applications.

I made this project maintainable, readable, and adaptable by structuring the code into clear class definitions (such as `TemperatureMachine` and `ManagedDisplay`), using descriptive naming conventions, maintaining a consistent commenting style, and ensuring that all hardware-specific behavior could easily be modified without rewriting core logic. This approach ensures that future developers can add new sensors, change outputs, or adapt the thermostat for cloud connectivity with minimal rework.

Overall, this project gave me a much deeper appreciation for how embedded systems development bridges hardware and software, and how critical good design and flexibility are for real-world product success.


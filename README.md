# SystemMonitorer

This system is designed to monitor system status on a basic level. First implementation contains an agent drawing system status information and sending it to external backend, which validates, saves and forwards it through APIs for a dashboard to display

Later this will be extended to be a containerized application including further information and easy distribution across systems, which can collectively be used and handled using different tools. More on that later as progression happens.

Running the application:

for development time there is a project root script run.py to run api and agent modules for interfaces and data collection.

UI can be run from frontend directory by npm run dev
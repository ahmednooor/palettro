# palettro

This app allows you to create color schemes which you can share with your friends and coworkers

#Installation

Just make sure you have `python` and `pip` installed already

- Run `pip install -r requirements.txt`
- Run `python app.py -p 8900` where `-p` param is for the port you want to run it on

You can view your app running after above steps at http://0.0.0.0:8900

#Using Docker 

- Make sure you have docker installed already. With new version of docker, you can simply use terminal for next steps.
- Run `docker build --rm -t fahdi/palettro .` You can change `-t` i.e tag param to whatever you like. Just make sure you use the same in next step
- Run `docker run -d -p 5984:8000 fahdi/palettro`. Note that `fahdi/palettro` is the name given in the previous step. Could be anything. The ` -p 5984:8000` parameter links the docker container's port `8000` to `5984` on your local machine. So, you can access the app at http://localhost:5984 now. 

# Build on Linux/ Unix

	 Note: You need docker installed already

- Make the build file executable with `chmod +x build.sh` or simply run `sh ./build.sh` to run the build script
- If you made the build script executable in previous step, run './build' and you are good to go. You can access the app at http://localhost:5984 after that

#Limitations 

The build process doesn't take already running containers of the previous builds into consideration. Since the port is static, we get port conflicts if some container is already using it. This will be solved in next releases. 




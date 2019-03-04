docker stop agentleaderauth
docker rm agentleaderauth
docker build -t agentleaderauth .
docker run -d -p 46400:46400 -p 46401:46401 --name agentleaderauth --restart unless-stopped agentleaderauth 

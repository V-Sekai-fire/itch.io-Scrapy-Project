# Update

```bash
bash
sudo apt-get update
sudo apt-get update && sudo apt-get install docker-compose-plugin
sudo usermod -aG docker $USER
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
sudo service docker start
docker rm -f marqo
docker pull marqoai/marqo:latest
# CPU only
docker run --name marqo -it --privileged -p 8882:8882 --add-host host.docker.internal:host-gateway marqoai/marqo:latest
pip install streamlit marqo
python3 first_index.py
python3 first_search.py
streamlit run text-image-search.py
```
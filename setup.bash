
sudo cp etc_systemd_system_jupyter-redirect.service /etc/systemd/system/jupyter-redirect.service;
sudo systemctl start jupyter-redirect;
sudo systemctl enable jupyter-redirect;

sudo cp _etc_nginx_sites-available_jupyter-redirect /etc/nginx/sites-available/jupyter-redirect;
sudo ln /etc/nginx/sites-available/jupyter-redirect /etc/nginx/sites-enabled;
sudo systemctl restart nginx;

sudo systemctl daemon-reload;
sudo systemctl restart jupyter-redirect;
sudo systemctl status jupyter-redirect;

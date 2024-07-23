conda create -n airflow_cdbr_new python=3.9 anaconda
conda activate airflow_cdbr_new

echo export PATH='$PATH':/home/cdbr/anaconda3/envs/airflow_cdbr_new/bin >> ~/.profile
echo export AIRFLOW_HOME=/home/cdbr/airflow/ >> ~/.bashrc

vi ~/airflow/airflow.cfg

vi ~/airflow/airflow.cfg
load_examples = False
auth_backend = airflow.api.auth.backend.basic_auth
endpoint_url = http://localhost:8083
base_url = http://localhost:8083
web_server_port = 8083

airflow db init
sudo ufw allow 8083

airflow users create --username cdbr --role Admin --password CDBRuser123 --email aceail0721@gmail.com --firstname Yeonjae --lastname Park

sudo vi /etc/systemd/system/airflow-webserver.service
[Unit]
Description=airflow scheduler

[Service]
User=cdbr
Type=simple
ExecStart=/home/cdbr/anaconda3/envs/airflow_cdbr_new/bin/airflow webserver
Restart=on-failure
RestartSec=5s
PrivateTmp=true

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl enable airflow-webserver
sudo systemctl start airflow-webserver
systemctl status airflow-webserver

sudo vi /etc/systemd/system/airflow-scheduler.service

[Unit]
Description=airflow webserver

[Service]
Environment="PATH=$PATH:/home/cdbr/anaconda3/envs/airflow_cdbr_new/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin"
User=cdbr
Type=simple
ExecStart=/home/cdbr/anaconda3/envs/airflow_cdbr_new/bin/airflow scheduler
Restart=on-failure
RestartSec=5s
PrivateTmp=true

[Install]
WantedBy=multi-user.target

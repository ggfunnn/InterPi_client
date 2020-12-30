import daemon as d
import interpi_client

daemon = interpi_client.Button_daemon()

with d.DaemonContext():
    daemon.initialize()
    daemon.wait()

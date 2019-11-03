import yaml
from google.cloud import storage
from service_pkg.file_io import load_data_pkl

BUCKET = "dkisler-sellics-settings"
path = "v1/params.yaml"


if __name__ == "__main__":
  gs = storage.Client()

  config_test = gs.get_bucket(BUCKET)\
                  .get_blob(path)\
                  .download_as_string()
  
  config = yaml.safe_load(config_test)
  print(config)

def load_config(file_path):
    import yaml
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    # Example usage
    config = load_config("config/kafka_config.yml")
    print(config)
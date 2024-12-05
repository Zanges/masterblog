import json
import os

from dataprovider.idataprovider import IDataProvider


class JsonProvider(IDataProvider):
    def __init__(self, file_path):
        if not file_path.endswith(".json"):
            raise ValueError("File must be a json file")
        path_without_filename = os.path.dirname(file_path)
        if not os.path.exists(path_without_filename):
            raise FileNotFoundError("Path does not exist")

        super().__init__()
        self._file_path = file_path

    def get_data(self: "JsonProvider") -> list[dict]:
        """Get all data from the json file"""
        if not os.path.exists(self._file_path):
            return []
        with open(self._file_path, "r") as file:
            content = file.read()
        return json.loads(content)

    def _save_data(self: "JsonProvider", data: list[dict]) -> None:
        """
        Save all data to the json

        :param data: data in form of list of dict
        """
        with open(self._file_path, "w") as file:
            file.write(json.dumps(data, indent=4))

    def get_data_by_id(self: "JsonProvider", post_id: int) -> dict | None:
        """
        Get data by id

        :param post_id: id of the post
        :return: data of the post
        """
        data = self.get_data()
        for item in data:
            if item["id"] == post_id:
                return item
        return None

    def add_data(self: "JsonProvider", data: dict) -> None:
        """
        Add data to the json

        :param data: data in form of dict
        """
        all_data = self.get_data()
        all_data.append(data)
        self._save_data(all_data)

    def update_data(self: "JsonProvider", post_id: int, data: dict) -> None:
        """
        Update data in the json

        :param post_id: id of the post to update
        :param data: new data in form of dict
        """
        all_data = self.get_data()
        for item in all_data:
            if item["id"] == post_id:
                item.update(data)
                break
        self._save_data(all_data)

    def delete_data(self: "JsonProvider", post_id: int) -> None:
        """
        Delete data from the json

        :param post_id: id of the post to delete
        """
        all_data = self.get_data()
        all_data = [item for item in all_data if item["id"] != post_id]
        self._save_data(all_data)

    def get_first_free_id(self: "JsonProvider") -> int:
        """
        Get the first free id

        :return: first free id
        """
        data = self.get_data()
        ids = [item["id"] for item in data]
        i = 0
        while True:
            if i not in ids:
                return i
            i += 1


def main():
    provider = JsonProvider("../data2.json")
    data = provider.get_data()
    print(data)


if __name__ == "__main__":
    main()
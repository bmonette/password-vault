class Account:
    """
    Represents a single account entry inside the password vault.
    """

    def __init__(self, name: str, username: str, password: str, notes: str = "", category: str = ""):
        self.name = name
        self.username = username
        self.password = password
        self.notes = notes
        self.category = category

# Example:
#
# Account(
#     name="Gmail",
#     username="johndoe@gmail.com",
#     password="password123",
#     notes="2FA on phone",
#     category="Personal"
# )

    def to_dict(self) -> dict:
        """
        Convert the Account object into a dictionary for JSON serialization.
        """

        return {
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "notes": self.notes,
            "category": self.category,
        }


    @staticmethod
    def from_dict(data: dict):
        """
        Create an Account object from a dictionary (after decryption).
        """

        return Account(
            name=data.get("name", ""),
            username=data.get("username", ""),
            password=data.get("password", ""),
            notes=data.get("notes", ""),
            category=data.get("category", ""),
        )

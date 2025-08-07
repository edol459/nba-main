class MockScoreBoard:
    def get_dict(self):
        return {
            "scoreboard": {
                "games": [
                    {
                        "gameId": "0022401044",
                        "gameStatus": 3  # Status 3 = final
                    }
                ]
            }
        }
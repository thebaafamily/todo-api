
from typing_extensions import Self

import pandas as pd

class DBUtil:
    __connection = None

    def __InitConnection(self) -> int:
        return 1

    def DBUtil(self):
        self.__connection = self.__InitConnection()

    def SelectQuery(self, query: str) -> pd.DataFrame:
        results = pd.DataFrame()
        return results

    def InsertData(self, df: pd.DataFrame) -> int:
        return 1
    
    def UpdateData(self, query: str) -> int:
        return 1


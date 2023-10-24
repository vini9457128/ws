from abc import ABC
from pprint import pprint
from datetime import datetime


class BaseAds(ABC):
    def __init__(self):
        self._memory = {}
        self.diff_in_minutes = 0

    def _save_references_in_memory(self, updated_campaings):

        # print(updated_campaings)

        # 17:30 -> sold 10,00(NOW)
        # 17:35 -> sold 15,00(NOW) sold  5,00  last  5 minutes
        # 17:45 -> sold 15,00(NOW) sold  0,00  last 15 minutes
        # 18:00 -> sold 25,00(NOW) sold 10,00  last 30 minutes
        # 18:00 -> sold 35,00(NOW)
        # 18:05 -> sold 40,00(NOW) sold  5,00  last  5 minutes

        for campaign_name in updated_campaings:

            # campanhas {campaign_name: {{'clicks': 2, 'leads': 2}}}

            if campaign_name not in self._memory:
                self._memory[campaign_name] = {}

            has_memory_reference = self._memory.get(
                campaign_name).get("memory_reference")

            if not has_memory_reference:
                self._memory[campaign_name]["memory_reference"] = {}
                self._memory[campaign_name]["memory_reference"].update(
                    updated_campaings[campaign_name])

                self._memory[campaign_name]["memory_reference"]["date"] = datetime.now(
                )

            # TODO: CHANGE: .seconds // 60 (for minutes)
            self.diff_in_minutes = (datetime.now(
            ) - self._memory[campaign_name]["memory_reference"]["date"]).seconds

            # print("time", self.diff_in_minutes)

            campaign_memory = self._memory.get(campaign_name)

            if self.diff_in_minutes >= 30:
                if not campaign_memory.get("last_thirty_minutes"):
                    self._memory[campaign_name]["last_thirty_minutes"] = {
                    }

                    self._memory[campaign_name]["last_thirty_minutes"].update(
                        updated_campaings[campaign_name])
                    self._memory[campaign_name]["last_thirty_minutes"]["date"] = datetime.now(
                    )

                    self._format_in_memory_values()

                # reset memory reference
                self._memory[campaign_name]["memory_reference"] = None

            elif self.diff_in_minutes >= 15:
                if not campaign_memory.get("last_fiveteen_minutes"):
                    self._memory[campaign_name]["last_fiveteen_minutes"] = {
                    }

                    self._memory[campaign_name]["last_fiveteen_minutes"].update(
                        updated_campaings[campaign_name])
                    self._memory[campaign_name]["last_fiveteen_minutes"]["date"] = datetime.now(
                    )

                    self._format_in_memory_values()

            elif self.diff_in_minutes >= 5:
                if not campaign_memory.get("last_five_minutes"):
                    self._memory[campaign_name]["last_five_minutes"] = {
                    }

                    self._memory[campaign_name]["last_five_minutes"].update(
                        updated_campaings[campaign_name])
                    self._memory[campaign_name]["last_five_minutes"]["date"] = datetime.now(
                    )

                    self._format_in_memory_values()

        # pprint(self._memory)
        return

    def _format_in_memory_values(self):

        for campaign_name, data in self._memory.items():
            # print("campaign_name", campaign_name)

            def is_valid(value):
                if value in ["id, date, device, status, optimization_score"]:
                    return False

                return isinstance(value, (int, float))

            # print(self._memory[campaign_name]["memory_reference"])
            memory_reference = self._memory[campaign_name]["memory_reference"]
            # return

            if self._memory.get(campaign_name).get("last_five_minutes"):
                print("cai no if")
                for k, v in data["last_five_minutes"].items():
                    print(k, is_valid(memory_reference[k]))

                    # if k in memory_reference and is_valid(memory_reference[k]):
                    #     print("cai no if interno")
                    #     print(
                    #         f"diferença de {k} foi {memory_reference[k] - v}")

                    #     self._memory[campaign_name]["last_five_minutes"][k] = memory_reference[k] - v

            else:
                print("eu n existo")

            # if self._memory.get(campaign_name).get("last_fiveteen_minutes"):

            #     for k, v in self._memory[campaign_name]["last_fiveteen_minutes"]:
            #         if k in memory_reference and is_valid(v) and memory_reference[k] < v:
            #             self._memory[campaign_name]["last_fiveteen_minutes"][k] = memory_reference[k] - v

            # if self._memory.get(campaign_name).get("last_thirty_minutes"):

            #     for k, v in self._memory[campaign_name]["last_thirty_minutes"]:
            #         if k in memory_reference and is_valid(v) and memory_reference[k] < v:
            #             self._memory[campaign_name]["last_thirty_minutes"][k] = memory_reference[k] - v

        pprint(self._memory)

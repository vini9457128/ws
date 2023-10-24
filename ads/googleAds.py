from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from datetime import datetime, timedelta
from pathlib import Path
from pprint import pprint
from baseAds import BaseAds

# USER_AGENT = "leadtracker"
# CLIENT_ID = "415471048664-8ver7c1iocqdp4h9jf13edc9nqjt0qfi.apps.googleusercontent.com"
# CLIENT_SECRET = "7u_rOx7YSxOm2MfXEY5JgxyL"
# DEVELOPER_TOKEN = "OmjN322wIhGO1fbDvXBasA"
# USE_PROTO_PLUS = False

# _googleads_yaml = """
#             user_agent: leadtracker
#             client_id: 415471048664-8ver7c1iocqdp4h9jf13edc9nqjt0qfi.apps.googleusercontent.com
#             client_secret: 7u_rOx7YSxOm2MfXEY5JgxyL
#             refresh_token: 1//0h6SzFL7wJn_LCgYIARAAGBESNwF-L9IrXyfeOKkmcMgcv_94QA4C5pe7ixIqrRfqasQHhgrG9TVQY5eOlnfSJ2heaFkhNoAXqCc
#             developer_token: OmjN322wIhGO1fbDvXBasA
#             use_proto_plus: false
#         """


class GoogleAds(BaseAds):
    def __init__(self, customer_id):
        # self.customer_refresh_token = customer_refresh_token
        self.customer_id = customer_id
        self._metrics_today = {}
        super().__init__()

    def get_campaigns(self, client):
        ga_service = client.get_service("GoogleAdsService")

        query = """
                SELECT
                    campaign.id,
                    campaign.name
                FROM campaign
                ORDER BY campaign.id"""

        stream = ga_service.search_stream(
            customer_id=self.customer_id, query=query)

        campaings = {}

        for batch in stream:
            for row in batch.results:
                campaings[row.campaign.name] = {
                    "id": row.campaign.id
                }

        print(campaings)
        return campaings

    def get_campaigns_metrics(self, client):
        ga_service = client.get_service("GoogleAdsService")

        yesterday = datetime.now() - timedelta(days=1)
        today = datetime.now()

        query = f"""
                SELECT
                    campaign.id,
                    campaign.name,
                    campaign.campaign_budget,
                    campaign.optimization_score,
                    campaign.status,
                    metrics.impressions,
                    metrics.cost_micros,
                    metrics.ctr,
                    metrics.average_cpc,
                    metrics.clicks,
                    segments.date,
                    segments.device
                FROM campaign
                WHERE
                    segments.date = "{yesterday.strftime("%Y-%m-%d")}"
                ORDER BY campaign.id"""

        # query = """
        #         SELECT
        #             campaign.commission
        #         FROM campaign_bidding_strategy"""

        campaings = {}

        stream = ga_service.search_stream(
            customer_id=self.customer_id, query=query)

        for batch in stream:
            for row in batch.results:
                campaings[row.campaign.name] = {
                    "id": row.campaign.id,
                    "campaign_budget": row.campaign.campaign_budget,
                    "optimization_score": row.campaign.optimization_score,
                    "status": row.campaign.status,
                    "impressions": row.metrics.impressions,
                    "cost_micros": row.metrics.cost_micros,
                    "ctr": row.metrics.ctr,
                    "average_cpc": row.metrics.average_cpc,
                    "clicks": row.metrics.clicks,
                    "device": row.segments.device,
                    "date": row.segments.date,
                }

        # print(campaings)

        self._save_references_in_memory(
            updated_campaings=campaings)

        # self._format_in_memory_values()

        # pprint(self._metrics_today)

        return self.get_campaigns_metrics(googleads_client)
        # return True


if __name__ == "__main__":
    googleads_client = GoogleAdsClient.load_from_storage(
        path=Path(__file__).resolve().parent / "google-ads.yaml", version="v14")

    try:
        GoogleAds("1309808784").get_campaigns_metrics(googleads_client)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")

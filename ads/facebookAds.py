from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.customaudience import CustomAudience
from facebook_business.adobjects.user import User as FBUser

import json
from datetime import datetime, timedelta
import requests
import random

# # ESSE N TEM NADA DE INSIGHTS
access_token = "EAAKxZBuKX3BoBAA0MnyupYFEJkxlX9XYj22tXIpeBoSwlgOh6IQuxYg6FPXdh8QCuO5z09BTwPlZADonPtEkB2tAhmUvOEAREvByQBs8zknKQ6duu5tEF4TlB7aNhZA2ZBh9UBuvHBCgUEIwzTDF8vkjiJ2JV2qLfVwkrrelDEMhd4LtpFgUesxVti5IDB7jwuZAsK2fnHqR6BZAvP3pK9MwkZCeRQhZBN34sbyTh3hHZCT0dgseMpGBH"
default_fb_account_id = "act_1169556923743324"

# # ESSE TEM INSIGHTS DEMAIS
# access_token = "EAAKxZBuKX3BoBAFUJgl8kaREDuJElhAT0iadRW94OH9D7mPNNChw0YODS0fD85lZBrooE14cTNRZBmoLcDQEeAzn0wK52ZBzfFxPVZAP8Soqpj6ZAGsRXq6eSfE5gx78XNoCQ2wUxvQIu4dqXScVJuRq9UZAV5qNTJ8c2O8PsNZANdg0YcVuZC4VF"
# default_fb_account_id = "act_227656818177490"

#  COREWORKERS => (receber ID de LTM):  click, investimento, impressoes, (dados de campanha) // GADS / FADS
#  Recerb dos ultimos 60m


class Facebook:
    MY_APP_ID = '758641054964762'
    MY_APP_SECRET = '2b5e959eba748bb3310f074b2b1ad5b4'

    def __init__(self, fb_account_id, access_token):
        self.fb_account_id = fb_account_id
        self.access_token = access_token

        FacebookAdsApi.init(self.MY_APP_ID, self.MY_APP_SECRET, access_token)

    def check_limit_api():
        def get_limits_fb(access_token, account_fb_id):
            check = requests.get(
                'https://graph.facebook.com/v16.0/' + account_fb_id +
                '/insights?access_token=' + access_token)

            try:
                x_business_use_case_usage = json.loads(
                    check.headers['x-business-use-case-usage'])
            except:
                return 0, 0

            try:
                aux_data = list(x_business_use_case_usage.values())[0][0]
            except:
                aux_data = {}

            call = int(aux_data.get('call_count', 0))
            cpu = int(aux_data.get('total_cputime', 0))
            total = int(aux_data.get('total_time', 0))

            usage = max(call, cpu, total)

            estimated_time_to_regain_access = int(
                aux_data.get('estimated_time_to_regain_access', 0))

            return usage, estimated_time_to_regain_access

        percent_use_api, sleep_time_in_min = get_limits_fb(
            access_token, default_fb_account_id)

        print('percent_use_api=', percent_use_api,
              'sleep_time_in_min=', sleep_time_in_min)

        return percent_use_api, sleep_time_in_min

    # FBuser

    def get_facebook_ads_accounts():

        fb_me = FBUser(fbid='me')
        ad_accounts = fb_me.get_ad_accounts(
            fields=[AdAccount.Field.name, AdAccount.Field.id])

        result = {}

        for ad_account in ad_accounts:
            result[ad_account["name"]] = {
                "id": ad_account.get("id"),
                "name": ad_account.get("name"),
            }

        return result

    def get_facebook_accounts(self):
        fb_me = FBUser(fbid='me')
        accounts = fb_me.get_accounts(
            fields=[AdAccount.Field.name, AdAccount.Field.id])

        result = {}

        for account in accounts:
            result[account["name"]] = {
                "id": account.get("id"),
                "name": account.get("name"),
            }

        return result

    # AdAccount

    def get_facebook_campaings_from_all_accounts():

        result = {}

        for ad_account in Facebook.get_facebook_ads_accounts().values():

            result[ad_account["name"]] = {
                "id": Facebook.get_facebook_campaings(ad_account.get("id"))
            }

        return json.dumps(result)

    def get_facebook_campaings(account_id=default_fb_account_id):

        fb_account = AdAccount(account_id)
        campaings = list(fb_account.get_campaigns(
            fields=[Campaign.Field.name, Campaign.Field.objective],
            params=({"is_completed": False}))
        )

        result = {}

        for campaing in campaings:
            result[campaing["id"]] = {
                "id": campaing.get("id"),
                "name": campaing.get("name"),
                "objective": campaing.get("objective"),
            }

        return json.dumps(result)

    def get_facebook_insight():

        fb_account = AdAccount(default_fb_account_id)
        insights = list(fb_account.get_insights())

        # sem insights para TNM
        return insights

    def get_facebook_ads():

        fb_account = AdAccount(default_fb_account_id)
        ads = list(fb_account.get_ads(fields=[Ad.Field.name]))

        result = {}

        for ad in ads:
            result[ad["name"]] = {
                "id": ad.get("id"),
                "name": ad.get("name"),
            }

        return json.dumps(result)

    def get_facebook_ads_sets():

        fb_account = AdAccount(default_fb_account_id)
        ad_sets = list(fb_account.get_ads(
            fields=[AdSet.Field.campaign, AdSet.Field.name, AdSet.Field.targeting]))

        result = {}

        for ad_set in ad_sets:
            result[ad_set["name"]] = {
                "id": ad_set.get("id"),
                "name": ad_set.get("name"),
                "campaign": ad_set.get("campaign"),
                "targeting": ad_set.get("targeting"),
            }

        return result

    def get_facebook_ad_images():

        fb_account = AdAccount(default_fb_account_id)
        ad_images = list(fb_account.get_ad_images())

        result = []

        for ad_image in ad_images:
            result.append((ad_image["hash"], ad_image["id"]))

        return json.dumps(result)

    def get_facebook_ad_creatives():

        fb_account = AdAccount(default_fb_account_id)
        ad_creatives = list(fb_account.get_ad_creatives(
            fields=[AdCreative.Field.body, AdCreative.Field.name]))

        result = {}

        for ad_creative in ad_creatives:
            result[ad_creative["name"]] = {
                "id": ad_creative.get("id"),
                "name": ad_creative.get("name"),
                "body": ad_creative.get("body"),
            }

        return json.dumps(result)

    def get_facebook_ad_videos():
        fb_account = AdAccount(default_fb_account_id)
        ad_videos = list(fb_account.get_ad_videos())

        result = {}

        for ad_video in ad_videos:
            result[ad_video.get("id")] = {
                "id": ad_video.get("id"),
                "updated_time": ad_video.get("updated_time"),
            }

        return result

    def get_facebook_custom_audiences():
        fb_account = AdAccount(default_fb_account_id)
        custom_audiences = list(fb_account
                                .get_custom_audiences(fields=[CustomAudience.Field.approximate_count_upper_bound,
                                                              CustomAudience.Field.approximate_count_lower_bound,
                                                              CustomAudience.Field.description,
                                                              CustomAudience.Field.data_source,
                                                              CustomAudience.Field.delivery_status,
                                                              ]))

        result = {}

        for custom_audience in custom_audiences:
            result[custom_audience.get("id")] = {
                "id": custom_audience.get("id"),
                "approximate_count_upper_bound": custom_audience.get("approximate_count_upper_bound"),
                "approximate_count_lower_bound": custom_audience.get("approximate_count_lower_bound"),
                "description": custom_audience.get("description"),
                "data_source": custom_audience.get("data_source"),
                "delivery_status": custom_audience.get("delivery_status"),
            }

        return result

    def get_facebook_users():
        fb_account = AdAccount(default_fb_account_id)
        users = list(fb_account.get_users())

        result = {}

        for user in users:
            result[user.get("name")] = {
                "id": user.get("id"),
                "name": user.get("name"),
                "tasks": user.get("tasks"),
            }

        return result

    def test_insights_last_minute(self, adset_id=None):

        # fb_account = AdAccount(self.fb_account_id)

        start_date = datetime.now() - timedelta(hours=1)
        end_date = datetime.now()

        params = {
            'time_range': {
                'since': start_date.strftime("%Y-%m-%d"),
                'until': end_date.strftime("%Y-%m-%d")
            },
        }

        if adset_id:

            ad_set_insights = AdSet(adset_id).get_insights(fields=[
                AdsInsights.Field.spend,
                AdsInsights.Field.impressions,
                AdsInsights.Field.actions,
                AdsInsights.Field.clicks,
                AdsInsights.Field.cost_per_ad_click,
                AdsInsights.Field.cost_per_conversion,
            ], params=params)

            result = []

            # return ad_set_insights.__getitem__()

            for ad_set_insight in ad_set_insights:

                result.append({
                    'spend': ad_set_insight.get(AdsInsights.Field.spend),
                    'impressions': ad_set_insight.get(AdsInsights.Field.impressions),
                    'actions': ad_set_insight.get(AdsInsights.Field.actions),
                    'clicks': ad_set_insight.get(AdsInsights.Field.clicks),
                    'cost_per_ad_click': ad_set_insight.get(AdsInsights.Field.cost_per_ad_click),
                    'cost_per_conversion': ad_set_insight.get(AdsInsights.Field.cost_per_conversion)
                })

            return {
                "title": f"INSIGHTS LAST MINUTE FOR ADSET {adset_id}",
                "result": result
            }

    def adset_insights_last_minute(self, adset_id=None):

        # fb_account = AdAccount(self.fb_account_id)

        start_date = datetime.now() - timedelta(minutes=1)
        end_date = datetime.now()

        params = {
            'time_range': {
                'since': start_date.strftime("%Y-%m-%d"),
                'until': end_date.strftime("%Y-%m-%d")
            },
        }

        if adset_id:

            ad_set_insights = AdSet(adset_id).get_insights(fields=[
                AdsInsights.Field.spend,
                AdsInsights.Field.impressions,
                AdsInsights.Field.actions,
                AdsInsights.Field.clicks,
                AdsInsights.Field.cost_per_ad_click,
                AdsInsights.Field.cost_per_conversion,
            ], params=params)

            # result = []

            for ad_set_insight in ad_set_insights:
                return {
                    'spend': ad_set_insight.get(AdsInsights.Field.spend),
                    'impressions': ad_set_insight.get(AdsInsights.Field.impressions),
                    'actions': ad_set_insight.get(AdsInsights.Field.actions),
                    'clicks': ad_set_insight.get(AdsInsights.Field.clicks),
                    'cost_per_ad_click': ad_set_insight.get(AdsInsights.Field.cost_per_ad_click),
                    'cost_per_conversion': ad_set_insight.get(AdsInsights.Field.cost_per_conversion)
                }

            # return {
            #     "title": f"INSIGHTS LAST MINUTE FOR ADSET {adset_id}",
            #     "result": result
            # }

    def ad_insights_last_minute(self, ad_id=None):

        # fb_account = AdAccount(self.fb_account_id)

        start_date = datetime.now() - timedelta(hours=1)
        end_date = datetime.now()

        params = {
            'time_range': {
                'since': start_date.strftime("%Y-%m-%d"),
                'until': end_date.strftime("%Y-%m-%d")
            },
        }

        if ad_id:

            ad_insights = Ad(ad_id).get_insights(fields=[
                AdsInsights.Field.spend,
                AdsInsights.Field.impressions,
                AdsInsights.Field.actions,
                AdsInsights.Field.clicks,
                AdsInsights.Field.cost_per_ad_click,
                AdsInsights.Field.cost_per_conversion,
            ], params=params)

            result = []

            for ad_insight in ad_insights:
                result.append({
                    'spend': ad_insight.get(AdsInsights.Field.spend),
                    'impressions': ad_insight.get(AdsInsights.Field.impressions),
                    'actions': ad_insight.get(AdsInsights.Field.actions),
                    'clicks': ad_insight.get(AdsInsights.Field.clicks),
                    'cost_per_ad_click': ad_insight.get(AdsInsights.Field.cost_per_ad_click),
                    'cost_per_conversion': ad_insight.get(AdsInsights.Field.cost_per_conversion)
                })

            return {
                "title": f"INSIGHTS LAST MINUTE FOR AD {ad_id}",
                "result": result
            }

    def campaign_insights_last_minute(self, campaign_id=None):

        # fb_account = AdAccount(self.fb_account_id)

        start_date = datetime.now() - timedelta(hours=1)
        end_date = datetime.now()

        params = {
            'time_range': {
                'since': start_date.strftime("%Y-%m-%d"),
                'until': end_date.strftime("%Y-%m-%d")
            },
        }

        if campaign_id:

            campaign_insights = Campaign(campaign_id).get_insights(fields=[
                AdsInsights.Field.spend,
                AdsInsights.Field.impressions,
                AdsInsights.Field.actions,
                AdsInsights.Field.clicks,
                AdsInsights.Field.cost_per_ad_click,
                AdsInsights.Field.cost_per_conversion,
            ], params=params)

            result = []

            for campaign_insight in campaign_insights:
                result.append({
                    'spend': campaign_insight.get(AdsInsights.Field.spend),
                    'impressions': campaign_insight.get(AdsInsights.Field.impressions),
                    'actions': campaign_insight.get(AdsInsights.Field.actions),
                    'clicks': campaign_insight.get(AdsInsights.Field.clicks),
                    'cost_per_ad_click': campaign_insight.get(AdsInsights.Field.cost_per_ad_click),
                    'cost_per_conversion': campaign_insight.get(AdsInsights.Field.cost_per_conversion)
                })

            return {
                "title": f"INSIGHTS LAST MINUTE FOR CAMPAIGN {campaign_id}",
                "result": result
            }


if __name__ == '__main__':

    facebookTest = Facebook('act_1169556923743324', 'EAAKxZBuKX3BoBAA0MnyupYFEJkxlX9XYj22tXIpeBoSwlgOh6IQuxYg6FPXdh8QCuO5z09BTwPlZADonPtEkB2tAhmUvOEAREvByQBs8zknKQ6duu5tEF4TlB7aNhZA2ZBh9UBuvHBCgUEIwzTDF8vkjiJ2JV2qLfVwkrrelDEMhd4LtpFgUesxVti5IDB7jwuZAsK2fnHqR6BZAvP3pK9MwkZCeRQhZBN34sbyTh3hHZCT0dgseMpGBH')

    outroUser = Facebook('act_227656818177490', 'EAAKxZBuKX3BoBAFUJgl8kaREDuJElhAT0iadRW94OH9D7mPNNChw0YODS0fD85lZBrooE14cTNRZBmoLcDQEeAzn0wK52ZBzfFxPVZAP8Soqpj6ZAGsRXq6eSfE5gx78XNoCQ2wUxvQIu4dqXScVJuRq9UZAV5qNTJ8c2O8PsNZANdg0YcVuZC4VF')

import requests
from pprint import pformat

cookies = {
    'JobseekerSessionId': '138ad246-8bda-4556-85e7-c453898f62a4',
    'JobseekerVisitorId': '138ad246-8bda-4556-85e7-c453898f62a4',
    '__cf_bm': '726nYh8BAvfj.26FTACBaUhjAo4W4_dKlEC.yfYgEVM-1790408190.8591564-1.0.1.1-oaSAK9_trZr4CTQB47BIvDRMrS..oIOl.wTEzIGlOEqiL3EKx5ScFS59xgonrfCBurxPmcdnKSqXe3ZwklydS6E.sija6QRQ9XmABMVE4GvrvVYMTLVBAeoJxFqhQXIZ',
    '_cfuvid': 'mlu_cD8ztPBgoJ0yGUwFTL0MLgQwzBYOfqUNWxR0fGU-1790408190.8591564-1.0.1.1-l26Gw2VMpgLOiGs2R51iTbiAGUBpwwXaUymZyKAh7T4',
    '_fbp': 'fb.1.1790408196988.874698062786869176',
    'sol_id': 'be4de6bb-dcdc-4f69-9c38-6e47a5582d54',
}

headers = {
    'accept': 'application/graphql-response+json,application/json;q=0.9',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://hk.jobsdb.com',
    'priority': 'u=1, i',
    'referer': 'https://hk.jobsdb.com/manager-jobs',
    'sec-ch-ua': '"Chromium";v="154", "Google Chrome";v="154", "Not A(Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'seek-request-brand': 'jobsdb',
    'seek-request-country': 'HK',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36',
    'x-custom-features': 'application/features.seek.all+json',
    'x-request-id': '9144903d-dfdd-42b4-89c8-e581bd72e63c',
    'x-seek-ec-sessionid': 'f06c080d-4b57-4bb5-859d-3fd1737fe2db',
    'x-seek-ec-visitorid': 'f06c080d-4b57-4bb5-859d-3fd1737fe2db',
    'x-seek-site': 'chalice',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'JobseekerSessionId=138ad246-8bda-4556-85e7-c453898f62a4; JobseekerVisitorId=138ad246-8bda-4556-85e7-c453898f62a4; __cf_bm=726nYh8BAvfj.26FTACBaUhjAo4W4_dKlEC.yfYgEVM-1790408190.8591564-1.0.1.1-oaSAK9_trZr4CTQB47BIvDRMrS..oIOl.wTEzIGlOEqiL3EKx5ScFS59xgonrfCBurxPmcdnKSqXe3ZwklydS6E.sija6QRQ9XmABMVE4GvrvVYMTLVBAeoJxFqhQXIZ; _cfuvid=mlu_cD8ztPBgoJ0yGUwFTL0MLgQwzBYOfqUNWxR0fGU-1790408190.8591564-1.0.1.1-l26Gw2VMpgLOiGs2R51iTbiAGUBpwwXaUymZyKAh7T4; _fbp=fb.1.1790408196988.874698062786869176; sol_id=be4de6bb-dcdc-4f69-9c38-6e47a5582d54',
}

json_data = {
    'operationName': 'JobSearchV7',
    'variables': {
        'params': {
            'searchIntent': {
                'country': 'HK',
                'locale': 'en-HK',
                'text': 'manager',
                'distanceKms': 2,
                'sort': 'score',
            },
            'searchContext': {
                'brand': 'jobsdb',
                'channel': 'web',
                'solVisitorId': 'be4de6bb-dcdc-4f69-9c38-6e47a5582d54',
                'intent': 'SEARCH',
                'source': 'FE_SERP',
            },
            'responseConfig': {
                'results': [
                    'jobs',
                ],
                'representations': [
                    'uiV1',
                ],
                'page': 3, ## page no.
                'pageSize': 60, ## page size.
                'enrichment': {
                    'suggestions': [
                        'locationV1',
                        'queryParamLabelsV1',
                        'sabFilterV1',
                        'organisationV1',
                        'spellingCorrectionV1',
                        'relatedSearchesV1',
                    ],
                    'relatedSearchesCount': 12,
                },
            },
            'sessionId': 'f06c080d-4b57-4bb5-859d-3fd1737fe2db',
        },
        'locale': 'en-HK',
        'zone': 'asia-1',
        'timezone': 'Asia/Hong_Kong',
        'country': 'HK',
        'tagsSubType': [
            'VSAB',
        ],
    },
    'extensions': {
        'clientLibrary': {
            'name': '@apollo/client',
            'version': '4.2.9',
        },
    },
    'query': 'query JobSearchV7($params: JobSearchV7QueryInput!, $locale: Locale!, $zone: Zone!, $country: JobSearchV7Country!, $timezone: Timezone!, $tagsSubType: [JobSearchV7TagsSubType!]) {\n  jobSearchV7(params: $params) {\n    results {\n      jobs {\n        id\n        title\n        abstract\n        adDisplay\n        advertiser {\n          id\n          name\n          __typename\n        }\n        organisation {\n          id\n          name\n          companyProfileId\n          companyProfileUrl\n          companyProfileRelativeUrlToBeUsedWithZone\n          __typename\n        }\n        categories {\n          id\n          label(locale: $locale)\n          __typename\n        }\n        location {\n          id\n          countryCode\n          displayName {\n            text\n            __typename\n          }\n          seoHierarchy {\n            contextualName {\n              text\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        cjs {\n          workTypes {\n            sourceId\n            name(locale: $locale)\n            __typename\n          }\n          source {\n            isAutoIncluded\n            __typename\n          }\n          salary {\n            hideSalary\n            minimum\n            maximum\n            currency\n            period\n            displayValue\n            __typename\n          }\n          roleTitles {\n            shortId\n            isDistinct\n            __typename\n          }\n          product {\n            branding {\n              companyLogoURL\n              __typename\n            }\n            bullets\n            adType {\n              sourceId\n              __typename\n            }\n            __typename\n          }\n          externalReferences {\n            id\n            sourceSystem\n            type\n            metadata {\n              name\n              assets {\n                profilePhotoUrl\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        listedAt {\n          dateTimeUtc\n          label(context: JOB_POSTED, length: SHORT, timezone: $timezone, locale: $locale)\n          __typename\n        }\n        salary {\n          period\n          min\n          max\n          currency\n          __typename\n        }\n        sol\n        tags(subType: $tagsSubType) {\n          type\n          label(locale: $locale)\n          __typename\n        }\n        url\n        workArrangements {\n          id\n          label {\n            lang\n            text\n            __typename\n          }\n          __typename\n        }\n        activity {\n          visitedApplicationSite {\n            count\n            mostRecent {\n              dateTimeUtc\n              __typename\n            }\n            __typename\n          }\n          applicationEnds {\n            count\n            mostRecent {\n              dateTimeUtc\n              __typename\n            }\n            __typename\n          }\n          applicationStarts {\n            count\n            mostRecent {\n              dateTimeUtc\n              __typename\n            }\n            __typename\n          }\n          impressions {\n            count\n            mostRecent {\n              dateTimeUtc\n              __typename\n            }\n            __typename\n          }\n          jobDetails {\n            count\n            mostRecent {\n              dateTimeUtc\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      pagination {\n        page\n        pageSize\n        resultCount\n        __typename\n      }\n      __typename\n    }\n    enrichment {\n      facets {\n        categoryV1 {\n          id\n          label {\n            lang\n            text\n            __typename\n          }\n          count\n          __typename\n        }\n        distinctTitleV1 {\n          id\n          label\n          count\n          __typename\n        }\n        __typename\n      }\n      suggestions {\n        queryParamLabelsV1 {\n          text\n          where {\n            id\n            kind\n            label {\n              lang\n              text\n              __typename\n            }\n            contextualName {\n              lang\n              text\n              __typename\n            }\n            contextualNameLocalisations(siteKey: $country) {\n              lang\n              text\n              __typename\n            }\n            isGranular\n            defaultDistanceKms\n            __typename\n          }\n          locationsHierarchy {\n            id\n            kind\n            label {\n              lang\n              text\n              __typename\n            }\n            contextualName {\n              lang\n              text\n              __typename\n            }\n            isGranular\n            defaultDistanceKms\n            __typename\n          }\n          __typename\n        }\n        relatedSearchesV1 {\n          totalJobs\n          text\n          __typename\n        }\n        organisationV1 {\n          organisationId\n          organisationName\n          totalJobs\n          __typename\n        }\n        locationV1 {\n          local {\n            sequence\n            completions {\n              id\n              label(locale: $locale, zone: $zone, context: CONTEXTUAL_NAME, labelType: SHORT)\n              __typename\n            }\n            __typename\n          }\n          international {\n            sequence\n            completions {\n              id\n              label(locale: $locale, zone: $zone, context: CONTEXTUAL_NAME, labelType: SHORT)\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        sabFilterV1 {\n          showSABFilter\n          __typename\n        }\n        canonicalV1 {\n          text\n          where {\n            id\n            name\n            __typename\n          }\n          __typename\n        }\n        spellingCorrectionV1 {\n          type\n          count\n          searchToken\n          label {\n            lang\n            defaultText\n            __typename\n          }\n          intent {\n            country\n            locale\n            text\n            where\n            whereId\n            sort\n            distanceKms\n            filter {\n              advertiserId\n              categoryId\n              listedAt\n              organisationId\n              organisationName\n              salaryMin\n              salaryMax\n              tags\n              workTypeId\n              workArrangementId\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    context {\n      searchToken\n      filterNewSince\n      representations {\n        uiV1 {\n          country\n          locale\n          text\n          where\n          whereId\n          sort\n          distanceKms\n          filter {\n            advertiserId\n            categoryId\n            categoryName\n            listedAt\n            organisationId\n            organisationName\n            salaryMin\n            salaryMax\n            tags\n            workTypeId\n            workArrangementId\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    metadata {\n      flight\n      request {\n        correlationId\n        __typename\n      }\n      sol\n      __typename\n    }\n    __typename\n  }\n}',
}

# response = requests.post('https://hk.jobsdb.com/graphql', cookies=cookies, headers=headers, json=json_data)

# print(f"Response: \n%s", pformat(response.json(), indent=4))


response_job_detail = requests.get('https://hk.jobsdb.com/job/94894477')

print(f"Response: {response_job_detail.text}")
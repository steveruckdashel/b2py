import base64, hashlib, json, requests

class b2:
    def __init__(id, key):
        self.id = id
        self.key = key
        self.session = requests.Session()

    def authorize_account():
        url = 'https://api.backblaze.com/b2api/v1/b2_authorize_account'
        id_and_key = '%s:%s' % (self.id, self.key)
        basic_auth_string = 'Basic ' + base64.b64encode(id_and_key)
        headers = { 'Authorization': basic_auth_string }

        r = self.session.get(url, headers=headers)
        response_data = r.json()

        self.auth_token = response_data['authorizationToken']
        self.api_url = response_data['apiUrl']
        self.download_url = response_data['downloadUrl']
        self.session.headers.update({'Authorization': response_data['authorizationToken']})

    def create_bucket(bucket_name, public=false):
        bucket_type = "allPublic" if public else "allPrivate"
        url = self.api_url + '/b2api/v1/b2_create_bucket'
        params = {
            'accountId': self.id,
            'bucketName': bucket_name,
            'bucketType': bucket_type
            }

        r = self.session.get(url, params=params)
        response_data = r.json()
        return response_data

    def delete_bucket(bucket_id):
        url = API_URL + '/b2api/v1/b2_delete_bucket'
        params = {
            'accountId': self.id,
            'bucketId': bucket_id
            }

        r = self.session.get(url, params=params)
        response_data = r.json()
        return response_data

    def list_buckets():
        url = self.api_url + '/b2api/v1/b2_list_buckets'
        params = { 'accountId': self.id }

        r = self.session.get(url, params=params)
        response_data = r.json()
        return response_data['buckets']

    def update_bucket(bucket_id, public=false):
        bucket_type = "allPublic" if public else "allPrivate"
        url = self.api_url + '/b2api/v1/b2_update_bucket'
        params = {
            'bucketId': bucket_id,
            'bucketType': bucket_type
            }

        r = self.session.get(url, params=params)
        response_data = r.json()
        return response_data

    def get_upload_url(bucket_id):
        url = self.api_url + '/b2api/v1/b2_get_upload_url'
        params = { 'bucketId': bucket_id }

        r = self.session.get(url, params=params)
        response_data = r.json()
        return response_data

    def upload_file(bucket_id, file_name, file_data, content_type):
        upload_url = get_upload_url(bucket_id)
        sha1_of_file_data = hashlib.sha1(file_data).hexdigest()
        headers = {
            'Authorization' : upload_url['authorizationToken'],
            'X-Bz-File-Name' :  file_name,
            'Content-Type' : content_type,
            'X-Bz-Content-Sha1' : sha1_of_file_data
            }

        r = self.session.post(upload_url['uploadUrl'], data=file_data, headers=headers)
        response_data = r.json()
        return response_data

    def list_file_names():
        url = self.api_url + '/b2api/v1/b2_list_file_names'
        params = { 'bucketId': bucket_id }

        r = self.session.get(url, params=params)
        response_data = r.json()
        return response_data

    def list_file_versions():
        url = self.api_url + "/b2api/v1/b2_list_file_versions"
        params = { 'bucketId': bucket_id }

        r = self.session.get(url, params=params)
        response_data = r.json()
        return response_data

    def download_file_by_id(file_id):
        url = self.download_url + "/b2api/v1/b2_download_file_by_id"
        params = { 'fileId' : file_id }
        r = self.session.get(url, params=params, stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            yield chunk

    def download_file_by_name(bucket_name, file_name):
        url = self.download_url + "/file/"+ bucket_name + "/" + file_name
        r = self.session.get(url, stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            yield chunk

    def delete_file_version(file_name, file_id):
        url = self.api_url + "/b2api/v1/b2_delete_file_version"
        params = { 'fileName' : file_name, 'fileId' : file_id }
        r = self.session.get(url, params=params)
        response_data = r.json()
        return response_data

    def get_file_info(file_id):
        url = self.api_url + "/b2api/v1/b2_get_file_info"
        params = { 'fileId' : file_id }
        r = self.session.get(url, params=params)
        response_data = r.json()
        return response_data

    def hide_file(bucket_id, file_name):
        url = self.api_url + "/b2api/v1/b2_hide_file"
        params = { 'bucketId' : bucket_id , 'fileName' : file_name }
        r = self.session.get(url, params=params)
        response_data = r.json()
        return response_data

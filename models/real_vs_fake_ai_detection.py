# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_predict_image_classification_sample]
import base64

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import image_compressor
import os
from dotenv import load_dotenv

load_dotenv()

project = os.getenv("PROJECT_PARAMS")
endpoint_id = os.getenv("ENDPOINT_ID")

if not project or not endpoint_id:
    raise ValueError("Environment variables PROJECT_PARAMS and ENDPOINT_ID must be set")

def predict_image_classification_sample(
    project: str,
    endpoint_id: str,
    filename: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    file_size = os.path.getsize(filename)
    if file_size > 1.45 * 1024 * 1024:
        image_compressor.compress_image(filename, filename)
    with open(filename, "rb") as f:
        file_content = f.read()

    # The format of each instance should conform to the deployed model's prediction input schema.
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageClassificationPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    # See gs://google-cloud-aiplatform/schema/predict/params/image_classification_1.0.0.yaml for the format of the parameters.
    parameters = predict.params.ImageClassificationPredictionParams(
        confidence_threshold=0.5,
        max_predictions=5,
    ).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    # print("response")
    # print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_classification_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    for prediction in predictions:
        array = dict(prediction)
    return array


# print(predict_image_classification_sample(
#     project=project,
#     endpoint_id=endpoint_id,
#     location="us-central1",
#     filename="models/test/fake_test/image_fx_-16.jpg"
# ))
# [END aiplatform_predict_image_classification_sample]
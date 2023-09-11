## AWS Sample: 

GenAI experimentation has been primarily with Large Langague Models (LLMs). With GenAI, it is also relatively simple to use Diffusion Models for Multimodal image synthesis.

This example uses Streamlit and Stable Diffusion XL to showcase a simple and intuitive user-interface. User provides an input image & some text to help guide generation of on output-image.  

Key features of this sample:
* Synthesise image using text-only prompt[s]
* Synthesies image using a mix of input-image and text prompt[s]
* Control the input-image strength towards the final output-image
* Generate/re-generate images on the fly
* Streamlit allows the App to be used on smart-phones and many other devices
* User can provide input-picture from their smart-phone camera or upload images from device storage.
* Download generated images onto local storage and/or S3 bucket

## Getting Started
1. Using SageMaker Jumpstart (Studio) deploy Stable Diffusion XL 1.0 model. Take a note of the endpoint-name (for example sdxl-jumpstart)
2. It is recommended to use a Cloud9 environment as it comes bundled with AWS CLI pre-installed. Create a Cloud9 environment
3. Streamlit runs on port 8501 by default, allow this in Security-Group associated with Cloud9 instance

Once the Cloud9 environment is setup, this example requires at least python 3.8. To install python 3.8:
```
sudo amazon-linux-extras install python3.8
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
```

Clone the sample repository:
```
'git clone https://github.com/aws-samples/amazon-aiml-genai-streamlit-stable-diffusion.git'
```

Download libraries & setup a virtual environment so all python dependencies are stored within project directory:
```
Admin:~/environment/amazon-aiml-genai-streamlit-stable-diffusion (main) $ ./download-dependencies.sh
Admin:~/environment/amazon-aiml-genai-streamlit-stable-diffusion (main) $ python -m venv .venv
Admin:~/environment/amazon-aiml-genai-streamlit-stable-diffusion (main) $ source .venv/bin/activate
(.venv) Admin:~/environment/amazon-aiml-genai-streamlit-stable-diffusion (main) $ pip install -r requirements.txt
```

Create a directory and file to store global password for the steamlit application:
```
Admin:~/environment/amazon-aiml-genai-streamlit-example (main) $ less .streamlit/secrets.toml

# .streamlit/secrets.toml

password = "Your-Password"
```

Update resources in the glib.py file:
```
# SM Jumpstart Consts
region_name = "us-west-2"
storage_bucket = "your-s3-storage"
sm_sdxl_ep = "sdxl-jumpstart"
```

Ensure that the Role/permissions associated with your Cloud9 instance can access:
1. SageMaker runtime
2. S3 bucket for output-image uploads 

## Now we run the sample streamlit application
To run the streamlit application, run the following command:
```
(.venv) Admin:~/environment/amazon-aiml-genai-streamlit-example (master) $ streamlit run genAI.py 

Collecting usage statistics. To deactivate, set browser.gatherUsageStats to False.


  You can now view your Streamlit app in your browser.

  Network URL: http://a.b.c.e:8501
  External URL: http://w.x.y.z:8501
```

Use a web browser to connect to the above streamlit app's URL

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.


# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.
#
# Assumptions: Object storage bucket already exists. See object_crud.py for an example of creating a bucket.
#              Loads configuration from default profile in the default config file

import oci
import os
import argparse
import zipfile
from datetime import date
from oci.signer import Signer
from multiprocessing import Process
from glob import glob

########## Configuration ####################
# Specify your config file
#TODO: replace with the path to your oci-cli config file
configfile = '~/config'

# Specify your profile name
# This Script assumes the profile name in the config file is DEFAULT but that can be changed here
profile = 'DEFAULT'

# Set true if using instance principal signing
use_instance_principal = 'TRUE'

# Set top level compartment OCID. Tenancy OCID will be set if null.
top_level_compartment_id = ''

# List target regions. All regions will be counted if null.
# target_region_names = ['us-ashburn-1']
target_region_names = []

#############################################

config = oci.config.from_file(configfile, profile)
tenancy_id = config['tenancy']
zipname = 'QBData' + date.today().strftime('%d_%m_%Y')

signer = Signer(
    tenancy = config['tenancy'],
    user = config['user'],
    fingerprint = config['fingerprint'],
    private_key_file_location = config['key_file'],
    pass_phrase = config['pass_phrase']
    )

object_storage = oci.object_storage.ObjectStorageClient(config)
namespace = object_storage.get_namespace().data # This gets the default namespace for the tenancy but can be changed to a specific namespace
bucket = '' #TODO: replace with bucket name 
file_path = "~/" + zipname #TODO: replace with desired file path for zip file
current_folder = '~/test' #TODO: replace with the path to folder to zip

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), 'Y:\\'))

def login(config, signer):
    identity = oci.identity.IdentityClient(config, signer=signer)
    user = identity.get_user(config['user']).data
    print("Logged in as: {} @ {}".format(user.description, config['region']))

def upload_to_object_storage(config, namespace, bucket, path):
    """
    upload_to_object_storage will upload a file to an object storage bucket.
    This function is intended to be run as a separate process.  The client is
    created with each invocation so that the separate processes do
    not have a reference to the same client.
    :param config: a configuration dictionary used to create ObjectStorageClient
    :param namespace: Namespace where the bucket resides
    :param bucket: Name of the bucket in which the object will be stored
    :param path: path to file to upload to object storage
    :rtype: None
    """
    with open(path, "rb") as in_file:
        name = os.path.basename(path)
        ostorage = oci.object_storage.ObjectStorageClient(config)
        ostorage.put_object(namespace,
                            bucket,
                            name,
                            in_file)
        print("Finished uploading {}".format(name))

print ("\n===========================[ Zip File ]=============================")
zipf = zipfile.ZipFile('zipname', 'w', zipfile.ZIP_DEFLATED)
zipdir(current_folder, zipf)
zip_file.close()
print ("\n===========================[ Login check ]=============================")
login(config, signer)
print ("\n===========================[ Upload check ]=============================")
# TODO: replace namespace, bucket and path
upload_to_object_storage(config, namespace, bucket, file_path)
print ("\n===========================[ Upload Coomplete! ]=============================")

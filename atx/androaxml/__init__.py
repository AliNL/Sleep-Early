#!/usr/bin/env python
# coding: utf-8

import zipfile
from xml.dom import minidom
from axmlparserpy.axmlprinter import AXMLPrinter


class Manifest(object):
    def __init__(self, content):
        self._dom = minidom.parseString(content)
        self._permissions = None

    @property
    def package_name(self):
        return self._dom.documentElement.getAttribute('package')

    @property
    def version_code(self):
        return self._dom.documentElement.getAttribute("android:versionCode")

    @property
    def version_name(self):
        return self._dom.documentElement.getAttribute("android:versionName")

    @property
    def permissions(self):
        if self._permissions is not None:
            return self._permissions

        self._permissions = []
        for item in self._dom.getElementsByTagName("uses-permission"):
            self._permissions.append(str(item.getAttribute("android:name")))
        return self._permissions

    @property
    def main_activity(self):
        """
        Returns:
            the name of the main activity
        """
        x = set()
        y = set()

        for item in self._dom.getElementsByTagName("activity"):
            for sitem in item.getElementsByTagName("action"):
                val = sitem.getAttribute("android:name")
                if val == "android.intent.action.MAIN":
                    x.add(item.getAttribute("android:name"))

            for sitem in item.getElementsByTagName("category"):
                val = sitem.getAttribute("android:name")
                if val == "android.intent.category.LAUNCHER":
                    y.add(item.getAttribute("android:name"))

        z = x.intersection(y)
        if len(z) > 0:
            return z.pop()
        return None


def parse_apk(filename):
    '''
    Returns:
        Manifest(Class)
    '''
    with zipfile.ZipFile(filename, 'r') as file:
        manifest = file.read('AndroidManifest.xml')
    return Manifest(AXMLPrinter(manifest).getBuff())
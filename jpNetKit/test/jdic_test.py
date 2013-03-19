#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lettuce import (
        step,
        world,
)

from src.jp.jdic import JDic

@step('I have the sentence "(.*)"')
def have_the_sentence(step, sentence):
    world.sentence = unicode(sentence)

@step('I query JDic API')
def query_jdic_api(step):
    world.response = JDic().lookup(world.sentence)

@step('I get (\d+) translated terms')
def get_list_of_three(step, expected):
    assert len(world.response) == int(expected), \
        "Got %d" % len(world.response)

@step('All translated terms are found in original sentence')
def all_terms_exist(step):
    for key in world.response.keys():
        assert key in world.sentence

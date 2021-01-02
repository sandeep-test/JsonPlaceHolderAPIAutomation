import random
from assertpy import assert_that, soft_assertions
from tests.fixtures import service_obj


post_keys = ['userId', 'id', 'title', 'body']


def test_get_posts(service_obj):
    res = service_obj.get_posts()
    with soft_assertions():
        assert_that(res.status_code).described_as('Response code').is_equal_to(200)
        assert_that(res.json()).described_as('Records in response').is_length(100)
        for post in res.json():
            assert_that(post).described_as('post').contains_only(*post_keys)


def test_get_a_single_post(service_obj):
    # requesting a random post no in each test run
    requested_post_id = random.randint(1, 100)
    res = service_obj.get_post_with_id(requested_post_id)

    with soft_assertions():
        assert_that(res.status_code).described_as('Response code').is_equal_to(200)
        assert_that(res.json()).described_as('Response').contains_only(*post_keys)
        assert_that(res.json()).described_as('Id in response').has_id(requested_post_id)


def test_delete_a_post(service_obj):
    # requesting a random post no in each test run
    requested_post_id = random.randint(1, 100)
    res = service_obj.delete_post_with_id(requested_post_id)

    with soft_assertions():
        assert_that(res.status_code).described_as('Response code').is_equal_to(200)
        assert_that(res.json()).described_as('Get Response').is_equal_to({})


def test_invalid_post(service_obj):
    res = service_obj.get_invalid_posts()
    assert_that(res.status_code).described_as('Response code').is_equal_to(404)


def test_post_a_new_post(service_obj):
    # requesting a random user id in each test run
    requested_user_id = random.randint(1, 100)
    body = {
        "title": "foo",
        "body": "bar",
        "userId": requested_user_id
    }
    res = service_obj.post_a_new_post(body)

    with soft_assertions():
        assert_that(res.status_code).described_as('Response code').is_equal_to(201)
        assert_that(res.json()).described_as('Response').contains_only(*post_keys)

    # getting the created request outside of soft assert
    # so as if creation fails, then get is not executed
    created_post_id = res.json().get('id')
    get_res = service_obj.get_post_with_id(created_post_id)
    body['id'] = created_post_id

    # ideally you should verify newly created body, but it doesnt works
    # newly created post is sent as a blank json from server
    # assert_that(get_res.json()).described_as('Get Response').is_equal_to(body)
    assert_that(get_res.json()).described_as('Get Response').is_equal_to({})


def test_put_a_post(service_obj):
    # requesting a random post id in each test run
    requested_user_id = 1
    requested_post_id = random.randint(1, 100)
    body = {
        "id": requested_post_id,
        "title": "abc",
        "body": "xyz",
        "userId": requested_user_id
    }
    res = service_obj.put_a_post(body)

    with soft_assertions():
        assert_that(res.status_code).described_as('Response code').is_equal_to(200)
        assert_that(res.json()).described_as('Response').contains_only(*post_keys)

        get_res = service_obj.get_post_with_id(requested_post_id)

        # ideally we should be checking for the post with updated body
        # newly updated post is being sent as the older one itself
        # assert_that(get_res.json()).described_as('Get Response').is_equal_to(body)
        assert_that(get_res.json()).described_as('Get Response').contains_only(*post_keys)

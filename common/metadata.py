health_route_metadata = dict(
    name="Health",
    description="You can perform health checks to see if the the service is live or "
    "not through the following routes.",
)
user_route_metadata = dict(
    name="User",
    description="Endpoints to create user and login user",
)
post_route_metadata = dict(
    name="Post",
    description="Endpoints to perform post related information",
)

tags_metadata = [
    health_route_metadata,
    user_route_metadata,
    post_route_metadata,
]

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.dataloader import DataLoader

@strawberry.type
class Hobby:
    id: int
    user_id: int
    name: str
    description: str | None

@strawberry.input
class CreateHobbyInput:
    user_id: int
    name: str
    description: str | None = None

hobbies: list[Hobby] = [
    Hobby(
        
        id=1,
        user_id=1,
        name="Reading",
        description="Reading books and articles"
    ),
    Hobby(
        id=2,
        user_id=1,
        name="Hiking",
        description="Exploring nature trails and mountains"
    ),
    Hobby(
        id=3,
        user_id=2,
        name="Cooking",
        description="Experimenting with new recipes and cuisines"
    )
]

async def load_hobbies_by_user(user_ids: list[int]) -> list[list[Hobby]]:
    result: list[list[Hobby]] = []
    for user_id in user_ids:
        user_hobbies = [hobby for hobby in hobbies if hobby.user_id == user_id]
        result.append(user_hobbies)
    return result


async def get_context():
    return {
        "hobbies_loader": DataLoader(
            load_fn = load_hobbies_by_user
        )
    }

@strawberry.type
class Query:
    @strawberry.field
    async def all_hobbies(self) -> list[Hobby]:
        return hobbies

    @strawberry.field
    async def hobby(self, hobby_id: int) -> Hobby | None:
        for hobby in hobbies:
            if hobby.id == hobby_id:
                return hobby
        return None

    @strawberry.field
    async def hobbies_by_user(self, info: strawberry.Info, user_id: int) -> list[Hobby]:
        return await info.context["hobbies_loader"].load(user_id)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_hobby(self, input: CreateHobbyInput) -> Hobby:
        new_hobby = Hobby(
            id=len(hobbies) + 1,
            user_id=input.user_id,
            name=input.name,
            description=input.description
        )
        hobbies.append(new_hobby)
        return new_hobby

schema = strawberry.Schema(
    query = Query,
    mutation = Mutation,
)

graphql_router = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_router, prefix="/graphql")
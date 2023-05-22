from rest_framework import serializers
from users.models import User, UserProfile
from .models import User, password_validator, password_pattern, user_name_validator, nickname_validator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from posts.serializers import PostSerializer
# from posts.models import Post
from django.contrib.auth.hashers import check_password

# from django.utils.http import urlsafe_base64_encode
# from django.core.mail import EmailMessage
# from django.utils.encoding import force_bytes
# from django.urls import reverse



# 회원가입에 필요한 serializer
class SignUpSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        error_messages={
            "required": "비밀번호 확인은 필수 입력 사항입니다!",
            "blank": "비밀번호 확인은 필수 입력 사항입니다!",
            "write_only": True,
        }
    )
    
    class Meta:
        model = User
        fields = (
            "user_name",
            "password",
            "re_password",
            "email",
        )
        extra_kwargs = {
            "user_name": {
                "error_messages": {
                    "required": "ID는 필수 입력 사항입니다!",
                    "blank": "ID는 필수 입력 사항입니다!",
                }
            },
            "password": {
                "write_only": True,
                "error_messages": {
                    "required": "비밀번호는 필수 입력 사항입니다!",
                    "blank": "비밀번호는 필수 입력 사항입니다!",
                },
            },
            "email": {
                "error_messages": {
                    "required": "email은 필수 입력 사항입니다!",
                    "invalid": "email 형식이 맞지 않습니다. 알맞은 형식의 email을 입력해주세요!",
                    "blank": "email은 필수 입력 사항입니다!",
                }
            },
        }

    def validate(self, data):
        user_name = data.get("user_name")
        password = data.get("password")
        re_password = data.get("re_password")

        # 아이디 유효성 검사
        if user_name_validator(user_name):
            raise serializers.ValidationError(detail={"username": "아이디는 6자 이상 30자 이하의 숫자, 영문 대/소문자를 포함하여야 합니다!"})

        # 비밀번호 & 비밀번호 확인 일치 검사
        if password != re_password:
            raise serializers.ValidationError(detail={"password": "비밀번호와 비밀번호 확인이 일치하지 않습니다!"})

        # 비밀번호 유효성 검사
        if password_validator(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 8자 이상의 영문 대소문자와 숫자, 특수문자를 포함하여야 합니다!"})

        # 비밀번호 유효성 검사
        if password_pattern(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 연속해서 3자리 이상 동일한 영문,숫자,특수문자 사용이 불가합니다!"})

        return data


    def create(self, validated_data):
        user_name = validated_data["user_name"]
        email = validated_data["email"]
        password = validated_data["password"]
        # 새로운 User 인스턴스를 생성과정에서 re_password가 예외를 발생시킬 수 있기 때문에 create() 메소드에서 check_password 필드를 제거합니다.
        validated_data.pop("re_password", None)
        user = User.objects.create(user_name=user_name, email=email,)
        
        user.set_password(password)
        user.save()
        
        # 새로운 사용자의 프로필을 생성하기 위해 UserProfile 모델에서 UserProfile 인스턴스를 생성합니다.
        UserProfile.objects.create(user=user)
        
        return validated_data


# 회원정보 수정에 필요한 serializer
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ("user_name",)
        extra_kwargs = {"user_name": {"error_messages": {"required": False, "blank": False,}},}

    def update(self, instance, validated_data):
        instance.user_name = validated_data.get("user_name", instance.user_name)
        instance.save()

        return instance


# 마이 페이지 serializer
class MyPageSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.user.email

    def get_user_name(self, obj):
        return obj.user.user_name

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user_id",
            "nickname",
            "profile_image",
            "email",
            "user_name",
            "introduction",
            "age",
            "gender",
            "review_cnt",
            "followers",
            "followings",
        )


# 마이 페이지 편집 serializer
class MyPageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "nickname",
            "profile_image",
            "introduction",
            "age",
            "gender",
        )
        extra_kwargs = {
            "nickname": {
                "error_messages": {
                    "required": "닉네임을 입력해주세요.",
                    "blank": "닉네임을 입력해주세요.",
                }
            },
            "introduction": {
                "error_messages": {
                    "required": "자기소개를 입력해주세요.",
                    "blank": "자기소개를 입력해주세요.",
                }
            },
        }

    def validate(self, data):
        nickname = data.get("nickname")

        # 닉네임 유효성 검사
        if nickname_validator(nickname):
            raise serializers.ValidationError(detail={"nickname": "닉네임은 3자이상 10자 이하로 작성해야하며 특수문자는 포함할 수 없습니다."})

        return data

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.profile_image = validated_data.get("profile_image", instance.profile_image)
        instance.introduction = validated_data.get("introduction", instance.introduction)
        instance.age = validated_data.get("age", instance.age)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.save()

        return instance


# 비밀번호 변경에 필요한 serializer
class ChangePasswordSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        error_messages={
            "required": "비밀번호 확인은 필수 입력 사항입니다!",
            "blank": "비밀번호 확인은 필수 입력 사항입니다!",
            "write_only": True,
        }
    )

    class Meta:
        model = User
        fields = (
            "password",
            "re_password",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "error_messages": {
                    "required": "비밀번호는 필수 입력 사항입니다!",
                    "blank": "비밀번호는 필수 입력 사항입니다!",
                },
            },
        }

    def validate(self, data):
        current_password = self.context.get("request").user.password
        password = data.get("password")
        re_password = data.get("re_password")

        # 현재 비밀번호와 바꿀 비밀번호 비교
        if check_password(password, current_password):
            raise serializers.ValidationError(detail={"password": "현재 사용 중인 비밀번호와 동일한 비밀번호입니다!"})

        # 비밀번호 & 비밀번호 확인 일치 검사
        if password != re_password:
            raise serializers.ValidationError(detail={"password": "비밀번호와 비밀번호 확인이 일치하지 않습니다!"})

        # 비밀번호 유효성 검사
        if password_validator(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 8자 이상의 영문 대소문자와 숫자, 특수문자를 포함하여야 합니다!"})

        # 비밀번호 유효성 검사
        if password_pattern(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 연속해서 3자리 이상 동일한 영문,숫자,특수문자 사용이 불가합니다!"})

        return data

    def update(self, instance, validated_data):
        instance.password = validated_data.get("password", instance.password)
        instance.set_password(instance.password)
        instance.save()

        return instance


# 로그인시 필요한 토큰 serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nickname'] = user.user_profile.nickname
        token["is_admin"] = user.is_admin
        return token
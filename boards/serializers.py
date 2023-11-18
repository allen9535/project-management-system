from rest_framework import serializers

from .models import Board, Column


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    # 보드를 그대로 직렬화하면 팀은 팀 id만 나옴
    # 따라서 별도의 메서드를 통해 어떤 값을 반환할지 결정함
    team = serializers.SerializerMethodField()
    # 보드에 컬럼과 관련된 값은 없지만, 컬럼은 보드를 외래키로 가지고 있음
    # 이를 활용해 원하는 값을 반환함
    column = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['team', 'column']

    # team 필드에 어떤 값을 반환할지 결정하는 메서드
    def get_team(self, obj):
        # 시리얼라이저에 들어온 보드 객체에서 팀명을 가져옴
        return obj.team.name

    # column 필드에 어떤 값을 반환할지 결정하는 메서드
    def get_column(self, obj):
        # 시리얼라이저에 들어온 보드 객체에 소속된 모든 컬럼을 오름차순으로 정렬
        columns = Column.objects.filter(board=obj).order_by('sequence')

        # 해당 데이터에서 필요한 내용만 딕셔너리 형태로 반환
        # {
        #    'team': '팀명',
        #    'column': {
        #       '컬럼명': 순서,
        #       '컬럼명': 순서,
        #        ...
        #     }
        # }
        column_data = {}
        for column in columns:
            column_data[column.id] = {
                'title': column.title,
                'sequence': column.sequence
            }

        return column_data

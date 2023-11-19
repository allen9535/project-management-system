from rest_framework import serializers

from .models import Board, Column, Ticket


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    # 보드를 그대로 직렬화하면 팀은 팀 id만 나옴
    # 따라서 별도의 메서드를 통해 어떤 값을 반환할지 결정함
    team = serializers.SerializerMethodField()
    # 보드에 티켓과 관련된 값은 없지만, 티켓은 컬럼을 외래키로, 컬럼은 보드를 외래키로 가지고 있음
    # 이를 활용해 원하는 값을 반환함
    column = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['team', 'column']

        # 해당 데이터에서 필요한 내용만 딕셔너리 형태로 반환
        # {
        #    'team': '팀명',
        #    'data': {
        #       '컬럼명': {
        #           'id': 컬럼 id,
        #           'sequence': 컬럼 순서
        #           'ticket': {
        #               '티켓명': {
        #                   'id': 티켓 id,
        #                   'charge': 담장자명,
        #                   'tag': 태그,
        #                   'sequence': 티켓 순서,
        #                   'volume': 작업량,
        #                   'ended_at': 마감일,
        #               }
        #           }
        #       }
        #        ...
        #     }
        # }

    # team 필드에 어떤 값을 반환할지 결정하는 메서드
    def get_team(self, obj):
        # 시리얼라이저에 들어온 보드 객체에서 팀명을 가져옴
        return obj.team.name

    # column 필드에 어떤 값을 반환할지 결정하는 메서드
    def get_column(self, obj):
        # 시리얼라이저에 들어온 보드 객체에 소속된 모든 컬럼을 오름차순으로 정렬
        columns = Column.objects.filter(board=obj).order_by('sequence')

        column_data = {}
        for column in columns:
            column_data[column.title] = {
                'id': column.id,
                'sequence': column.sequence
            }

            ticket_data = {}
            # 현재 컬럼에 해당하는 모든 티켓을 오름차순으로 정렬
            tickets = Ticket.objects.filter(column=column).order_by('sequence')
            for ticket in tickets:
                ticket_data[ticket.title] = {}

                try:
                    ticket_data[ticket.title] = {
                        'id': ticket.id,
                        'tag': ticket.tag,
                        'charge': ticket.charge.username,
                        'volume': ticket.volume,
                        'ended_at': ticket.ended_at,
                        'sequence': ticket.sequence
                    }
                except AttributeError:
                    ticket_data[ticket.title] = {
                        'id': ticket.id,
                        'tag': ticket.tag,
                        'charge': None,
                        'volume': ticket.volume,
                        'ended_at': ticket.ended_at,
                        'sequence': ticket.sequence
                    }

                column_data[column.title]['ticket'] = ticket_data

        return column_data

import streamlit as st
from supabase import create_client

st.set_page_config(page_title='Стена объявлений УУНиТ')
st.title('Новости и мероприятия УУНиТ')
st.write('Твой главный гид по кампусу: узнавай о событиях университета и находи направления по твоим интересам')
URL = 'https://prsionjsoghhfozqxjcc.supabase.co'
KEY = 'sb_publishable_T68UTH0pU6HCGCMo8JdD6A_HiiatgI0'
supabase = create_client(URL, KEY)


def get_news():
    try:
        res = supabase.table('posts').select('*').execute()
        return res.data
    except Exception as e:
        st.error(f'Ошибка бэка: {e}')
        return []


all_news = get_news()
if not all_news:
    st.info('Пока новостей нет, добавьте первую!')
else:
    tab_news, tab_events = st.tabs(['Новости', 'Мероприятия'])
    with tab_news:
        found_news = False
        for post in all_news:
            if post.get('category') == 'Новость':
                found_news = True
                with st.container(border=True):
                    st.subheader(f"{post.get('title', 'Без названия')}")
                    if post.get('event_date'):
                        st.markdown(f'**{post.get('event_date')}**')
                    if post.get('description'):
                        st.write(post.get('description'))
                    if post.get('link'):
                        st.link_button('Поподробнее', post.get('link'))
        if not found_news:
            st.write('Новостей пока нет')
    with tab_events:
        found_events = False
        for post in all_news:
            if post.get('category') == 'Мероприятие':
                found_events = True
                with st.container(border=True):
                    st.subheader(f'{post.get('title', 'Без названия')}')
                    if post.get('event_date') and post.get('event_date') != 'None':
                        st.markdown(f'**{post.get('event_date')}**')
                        if post.get('description'):
                            st.write(post.get('description'))
                        if post.get('link'):
                            st.link_button('Поподробнее', post.get('link'))
        if not found_news:
                st.write('Новостей пока нет')


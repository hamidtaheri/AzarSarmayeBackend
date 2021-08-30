use mahmodiyan4
go

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[All_Calcs] @Tbl_Pardakht_List_Id int, @countm int
AS
BEGIN
    delete from Tbl_Tarakonesh where Tbl_Tarakonesh.Tbl_Pardakht_List_id = @Tbl_Pardakht_List_Id

    declare @_id int
    DECLARE the_cursor CURSOR FAST_FORWARD
        FOR SELECT [id]
            FROM Tbl_Ashkhas

    OPEN the_cursor
    FETCH NEXT FROM the_cursor INTO @_id

    WHILE @@FETCH_STATUS = 0
        BEGIN

            EXEC [dbo].[Pardakht_Calc_Skhakhs]
                 @Tbl_Pardakht_List_Id = @Tbl_Pardakht_List_Id,
                 @id_Shakhs = @_id, @countmah=@countm

            FETCH NEXT FROM the_cursor INTO @_id
        END

    CLOSE the_cursor
    DEALLOCATE the_cursor

END
go

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE FUNCTION [dbo].[Get_Mande](
    @Tbl_Ashkhas_id int
)
    RETURNS bigint
AS
BEGIN
    return (isnull((select sum(Mablagh)
                    from Tbl_Tarakonesh
                    where Tbl_Ashkhas_id = @Tbl_Ashkhas_id and Tbl_Type_Vajh_id = 1), 0) + isnull((select sum(Mablagh)
                                                                                                   from Tbl_Tarakonesh
                                                                                                   where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                                                                                                     and Tbl_Type_Vajh_id = 3),
                                                                                                  0) - isnull(
                    (select sum(Mablagh)
                     from Tbl_Tarakonesh
                     where Tbl_Ashkhas_id = @Tbl_Ashkhas_id and Tbl_Type_Vajh_id = 2), 0) - isnull((select sum(Mablagh)
                                                                                                    from Tbl_Tarakonesh
                                                                                                    where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                                                                                                      and Tbl_Type_Vajh_id = 4),
                                                                                                   0) + isnull(
                    (select sum(Mablagh)
                     from Tbl_Tarakonesh
                     where Tbl_Ashkhas_id = @Tbl_Ashkhas_id and Tbl_Type_Vajh_id = 5), 0))

END
go

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE FUNCTION [dbo].[Get_Mande_By_Date](
    @Tbl_Ashkhas_id int, @Tarikh nvarchar(10)
)
    RETURNS bigint
AS
BEGIN
    return (isnull((select sum(Mablagh * DarMelyoon)
                    from Tbl_Tarakonesh
                    where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                      and Tbl_Type_Vajh_id = 1
                      and Tarikh_Moaser <= @Tarikh), 0) + isnull((select sum(Mablagh * DarMelyoon)
                                                                  from Tbl_Tarakonesh
                                                                  where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                                                                    and Tbl_Type_Vajh_id = 3
                                                                    and Tarikh_Moaser <= @Tarikh), 0) -
            isnull((select sum(Mablagh * DarMelyoon)
                    from Tbl_Tarakonesh
                    where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                      and Tbl_Type_Vajh_id = 2
                      and Tarikh_Moaser <= @Tarikh), 0) - isnull((select sum(Mablagh * DarMelyoon)
                                                                  from Tbl_Tarakonesh
                                                                  where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                                                                    and Tbl_Type_Vajh_id = 4
                                                                    and Tarikh_Moaser <= @Tarikh), 0) +
            isnull((select sum(Mablagh * DarMelyoon)
                    from Tbl_Tarakonesh
                    where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                      and Tbl_Type_Vajh_id = 5
                      and Tarikh_Moaser <= @Tarikh), 0)) / 10000000

END
go

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE FUNCTION [dbo].[Get_Mande_By_Date_Moaref](
    @Tbl_Ashkhas_id int, @Tarikh nvarchar(10)
)
    RETURNS bigint
AS
BEGIN
    return (isnull((select sum(Mablagh)
                    from Tbl_Tarakonesh
                    where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                      and Tbl_Type_Vajh_id = 1
                      and Tarikh_Moaser_Moaref <= @Tarikh), 0) + isnull((select sum(Mablagh)
                                                                         from Tbl_Tarakonesh
                                                                         where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                                                                           and Tbl_Type_Vajh_id = 3
                                                                           and Tarikh_Moaser_Moaref <= @Tarikh), 0) -
            isnull((select sum(Mablagh)
                    from Tbl_Tarakonesh
                    where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                      and Tbl_Type_Vajh_id = 2
                      and Tarikh_Moaser_Moaref <= @Tarikh), 0) - isnull((select sum(Mablagh)
                                                                         from Tbl_Tarakonesh
                                                                         where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                                                                           and Tbl_Type_Vajh_id = 4
                                                                           and Tarikh_Moaser_Moaref <= @Tarikh), 0) +
            isnull((select sum(Mablagh)
                    from Tbl_Tarakonesh
                    where Tbl_Ashkhas_id = @Tbl_Ashkhas_id
                      and Tbl_Type_Vajh_id = 5
                      and Tarikh_Moaser_Moaref <= @Tarikh), 0))

END
go

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE FUNCTION [dbo].[Get_Safte](
    @Tbl_Ashkhas_id int
)
    RETURNS bigint
AS
BEGIN
    return (isnull((select sum(Mablagh) from Tbl_Safte where Tbl_Ashkhas_id = @Tbl_Ashkhas_id), 0))

END
go

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[Pardakht_Calc_Skhakhs] @Tbl_Pardakht_List_Id int, @id_Shakhs int, @countmah int
AS
BEGIN

    declare @varibekhod bit=(select MorefiBekhod from Tbl_Ashkhas where Tbl_Ashkhas.id = @id_Shakhs)
    declare @varibekhod2 bit=(select MorefiBekhod2 from Tbl_Ashkhas where Tbl_Ashkhas.id = @id_Shakhs)
    declare @mz decimal(18, 4)=(select Mizan_Har_Melyoon from Tbl_Ashkhas where Tbl_Ashkhas.id = @id_Shakhs)
    declare @mz_m decimal(18, 4)=(select Mizan_Har_Melyoon_Moaref from Tbl_Ashkhas where Tbl_Ashkhas.id = @id_Shakhs)
    declare @m_id int=(select Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id from Tbl_Ashkhas where Tbl_Ashkhas.id = @id_Shakhs)

    declare @mz_m2 decimal(18, 4)=(select Mizan_Har_Melyoon_Moaref2 from Tbl_Ashkhas where Tbl_Ashkhas.id = @id_Shakhs)
    declare @m_id2 int=(select Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id2 from Tbl_Ashkhas where Tbl_Ashkhas.id = @id_Shakhs)


    Declare @az int
    Declare @ta int
    set @az = (select Az_Int from Tbl_Pardakht_List where id = @Tbl_Pardakht_List_Id)
    set @ta = (select Ta_Int from Tbl_Pardakht_List where id = @Tbl_Pardakht_List_Id)
    declare @mahcount decimal(18, 4)=(select Mah_Count from Tbl_Pardakht_List where id = @Tbl_Pardakht_List_Id)
    declare @pdate nvarchar(10)=(select Mah from Tbl_Pardakht_List where id = @Tbl_Pardakht_List_Id)

    declare @tarikh nvarchar(10)=(select Tarikh from Tbl_Pardakht_List where id = @Tbl_Pardakht_List_Id)
    declare @d nvarchar(10)
    declare @sood decimal(18, 4)=0
    declare @sood_Moref decimal(18, 4)=0
    declare @sood_Moref2 decimal(18, 4)=0


    declare @kosoorat bigint=(select Kosoorat from Tbl_Ashkhas where Tbl_Ashkhas.id = @id_Shakhs)


    while @az <= @ta
        begin
            set @d = SUBSTRING(@pdate, 0, 9) + RIGHT('00' + cast(@az as nvarchar(2)), 2)


--print @d

            declare @remian decimal(18, 4)
            set @remian = dbo.Get_Mande_By_Date(@id_Shakhs, @d)
--print @remian

            set @sood = @sood + (((@remian)) / @countmah)
            print @sood


            --
--print @sood_Moref
            set @az = @az + 1
        end


    set @az = (select Az_Int from Tbl_Pardakht_List where id = @Tbl_Pardakht_List_Id)
    set @ta = (select Ta_Int from Tbl_Pardakht_List where id = @Tbl_Pardakht_List_Id)


    while @az <= @ta
        begin
            set @d = SUBSTRING(@pdate, 0, 9) + RIGHT('00' + cast(@az as nvarchar(2)), 2)


--print @d

            declare @remian_moaref decimal(18, 4)
            set @remian_moaref = dbo.Get_Mande_By_Date_Moaref(@id_Shakhs, @d)
--print @remian


            set @sood_Moref = @sood_Moref + ((((@remian_moaref / 10000000) * @mz_m)) / @countmah)
            set @sood_Moref2 = @sood_Moref2 + ((((@remian_moaref / 10000000) * @mz_m2)) / @countmah)


            --
--print @sood_Moref
            set @az = @az + 1
        end


    declare @sood_b bigint =cast(round(@sood, -1) as bigint)
    declare @sood_Moref_b bigint =cast(round(@sood_Moref, -1) as bigint)
    declare @sood_Moref_b2 bigint =cast(round(@sood_Moref2, -1) as bigint)


    if (@kosoorat > 0)
        begin

            set @sood_b = @sood_b - @kosoorat
            update Tbl_Ashkhas set Kosoorat=0 where Tbl_Ashkhas.id = @id_Shakhs
        end


    if (@sood_b > 0)
        begin


            INSERT INTO [dbo].[Tbl_Tarakonesh]
            ( [Tbl_Ashkhas_id]
            , [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref]
            , [Time]
            , [Mablagh]
            , [Tbl_Type_Vajh_id]
            , [NahveyePardakht]
            , [Des]
            , [Tbl_Pardakht_List_id], [DarMelyoon])
            values (@id_Shakhs, @tarikh, @tarikh, @tarikh, getdate(), @sood_b, 3, '', 'واریز سود به صندوق',
                    @Tbl_Pardakht_List_Id, @mz)

            if ((select Daryaft_Sood from Tbl_Ashkhas where Tbl_Ashkhas.id = @id_Shakhs) = 1)
                begin

                    INSERT INTO [dbo].[Tbl_Tarakonesh]
                    ( [Tbl_Ashkhas_id]
                    , [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref]
                    , [Time]
                    , [Mablagh]
                    , [Tbl_Type_Vajh_id]
                    , [NahveyePardakht]
                    , [Des]
                    , [Tbl_Pardakht_List_id], [DarMelyoon])
                    values (@id_Shakhs, @tarikh, @tarikh, @tarikh, getdate(), @sood_b, 4, '', 'برداشت سود از صندوق',
                            @Tbl_Pardakht_List_Id, @mz)

                end
        end
    if (@sood_Moref_b > 0 and @m_id is not null)
        begin
            declare @idd int
            if (@varibekhod = 1)
                begin
                    set @idd = @id_Shakhs
                end
            else
                begin
                    set @idd = @m_id
                end


            declare @Kosoorat_Moarefi bigint=(select Kosoorat_Moarefi from Tbl_Ashkhas where Tbl_Ashkhas.id = @idd)

            if (@Kosoorat_Moarefi > 0)
                begin
                    set @sood_Moref_b = @sood_Moref_b - @Kosoorat_Moarefi
                    update Tbl_Ashkhas set Kosoorat_Moarefi=0 where Tbl_Ashkhas.id = @idd
                end


            declare @name1 nvarchar(100)=(select Fname + ' ' + Lname from Tbl_Ashkhas where id = @id_Shakhs)
            INSERT INTO [dbo].[Tbl_Tarakonesh]
            ( [Tbl_Ashkhas_id]
            , [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref]
            , [Time]
            , [Mablagh]
            , [Tbl_Type_Vajh_id]
            , [NahveyePardakht]
            , [Des]
            , [Tbl_Pardakht_List_id], [DarMelyoon])
            values (@idd, @tarikh, @tarikh, @tarikh, getdate(), @sood_Moref_b, 5, '', N' واریز سود معرفی یک ' + @name1,
                    @Tbl_Pardakht_List_Id, @mz_m)


            if ((select Daryaft_Sood from Tbl_Ashkhas where Tbl_Ashkhas.id = @m_id) = 1)
                begin

                    INSERT INTO [dbo].[Tbl_Tarakonesh]
                    ( [Tbl_Ashkhas_id]
                    , [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref]
                    , [Time]
                    , [Mablagh]
                    , [Tbl_Type_Vajh_id]
                    , [NahveyePardakht]
                    , [Des]
                    , [Tbl_Pardakht_List_id], [DarMelyoon])
                    values (@idd, @tarikh, @tarikh, @tarikh, getdate(), @sood_Moref_b, 4, '',
                            N' برداشت سود معرفی یک ' + @name1, @Tbl_Pardakht_List_Id, @mz_m)
                end


        end


    if (@sood_Moref_b2 > 0 and @m_id2 is not null)
        begin
            declare @idd2 int
            if (@varibekhod2 = 1)
                begin
                    set @idd2 = @id_Shakhs
                end
            else
                begin
                    set @idd2 = @m_id2
                end


            declare @Kosoorat_Moarefi2 bigint=(select Kosoorat_Moarefi from Tbl_Ashkhas where Tbl_Ashkhas.id = @idd)

            if (@Kosoorat_Moarefi > 0)
                begin
                    set @sood_Moref_b2 = @sood_Moref_b2 - @Kosoorat_Moarefi
                    update Tbl_Ashkhas set Kosoorat_Moarefi=0 where Tbl_Ashkhas.id = @idd
                end


            declare @name2 nvarchar(100)=(select Fname + ' ' + Lname from Tbl_Ashkhas where id = @id_Shakhs)
            INSERT INTO [dbo].[Tbl_Tarakonesh]
            ( [Tbl_Ashkhas_id]
            , [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref]
            , [Time]
            , [Mablagh]
            , [Tbl_Type_Vajh_id]
            , [NahveyePardakht]
            , [Des]
            , [Tbl_Pardakht_List_id], [DarMelyoon])
            values (@idd2, @tarikh, @tarikh, @tarikh, getdate(), @sood_Moref_b2, 5, '',
                    N' واریز سود معرفی دو ' + @name2, @Tbl_Pardakht_List_Id, @mz_m2)


            if ((select Daryaft_Sood from Tbl_Ashkhas where Tbl_Ashkhas.id = @m_id) = 1)
                begin

                    INSERT INTO [dbo].[Tbl_Tarakonesh]
                    ( [Tbl_Ashkhas_id]
                    , [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref]
                    , [Time]
                    , [Mablagh]
                    , [Tbl_Type_Vajh_id]
                    , [NahveyePardakht]
                    , [Des]
                    , [Tbl_Pardakht_List_id], [DarMelyoon])
                    values (@idd2, @tarikh, @tarikh, @tarikh, getdate(), @sood_Moref_b2, 4, '',
                            N' برداشت سود معرفی دو ' + @name2, @Tbl_Pardakht_List_Id, @mz_m2)
                end


        end


END
go

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE FUNCTION [dbo].[getbank](
    @id int
)
    RETURNS TABLE
        AS
        RETURN
            (
                select id, pardakhti as PardakhtiKhod, 0 as pardakhti
                from getbank_VarizBeMoaref0(@id)
                union all
                select Moaref_Tbl_Ashkhas_id, 0 as PardakhtiKhod, pardakhti
                from getbank_VarizBeMoaref1(@id)
            )
go

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
create FUNCTION [dbo].[getbank_Koli](
    @id int
)
    RETURNS TABLE
        AS
        RETURN
            (
                SELECT Tbl_Ashkhas.id, SUM(Tbl_Tarakonesh.Mablagh) AS Pardakhti, Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id
                FROM Tbl_Ashkhas
                         INNER JOIN
                     Tbl_Tarakonesh ON Tbl_Ashkhas.id = Tbl_Tarakonesh.Tbl_Ashkhas_id
                WHERE (Tbl_Tarakonesh.Tbl_Pardakht_List_id = @id)
                  AND (Tbl_Tarakonesh.Tbl_Type_Vajh_id = 4)
                GROUP BY Tbl_Ashkhas.id, Moaref_Tbl_Ashkhas_id
                HAVING (SUM(Tbl_Tarakonesh.Mablagh) > 0)
            )
go

-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE FUNCTION [dbo].[getbank_VarizBeMoaref0](
    @id int
)
    RETURNS TABLE
        AS
        RETURN
            (
                SELECT Tbl_Ashkhas.id, SUM(Tbl_Tarakonesh.Mablagh) AS Pardakhti
                FROM Tbl_Ashkhas
                         INNER JOIN
                     Tbl_Tarakonesh ON Tbl_Ashkhas.id = Tbl_Tarakonesh.Tbl_Ashkhas_id
                WHERE (Tbl_Tarakonesh.Tbl_Pardakht_List_id = @id)
                  AND (Tbl_Tarakonesh.Tbl_Type_Vajh_id = 4)
                  and Tbl_Ashkhas.VarizBeMoaref = 0
                GROUP BY Tbl_Ashkhas.id
                HAVING (SUM(Tbl_Tarakonesh.Mablagh) > 0)
            )
go

create FUNCTION [dbo].[getbank_VarizBeMoaref1](
    @id int
)
    RETURNS TABLE
        AS
        RETURN
            (
                SELECT Tbl_Ashkhas.id, SUM(Tbl_Tarakonesh.Mablagh) AS Pardakhti, Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id
                FROM Tbl_Ashkhas
                         INNER JOIN
                     Tbl_Tarakonesh ON Tbl_Ashkhas.id = Tbl_Tarakonesh.Tbl_Ashkhas_id
                WHERE (Tbl_Tarakonesh.Tbl_Pardakht_List_id = @id)
                  AND (Tbl_Tarakonesh.Tbl_Type_Vajh_id = 4)
                  and Tbl_Ashkhas.VarizBeMoaref = 1
                GROUP BY Tbl_Ashkhas.id, Moaref_Tbl_Ashkhas_id
                HAVING (SUM(Tbl_Tarakonesh.Mablagh) > 0)
            )
go

-------
CREATE VIEW [dbo].[View_AllAshkhas_With_Mande]
AS
SELECT        dbo.Tbl_Ashkhas.id, dbo.Tbl_Ashkhas.Fname, dbo.Tbl_Ashkhas.Lname, dbo.Tbl_Ashkhas.CodeMeli, dbo.Tbl_Ashkhas.Adress, dbo.Tbl_Ashkhas.ShomareKart, dbo.Tbl_Ashkhas.Hesab, dbo.Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id,
                         dbo.Tbl_Ashkhas.Mizan_Har_Melyoon, dbo.Tbl_Ashkhas.Mizan_Har_Melyoon_Moaref, dbo.Tbl_Ashkhas.Daryaft_Sood, CAST(dbo.Get_Safte(dbo.Tbl_Ashkhas.id) AS decimal(18, 0)) AS Safte,
                         CAST(dbo.Get_Mande(dbo.Tbl_Ashkhas.id) AS decimal(18, 0)) AS Mande, Tbl_Ashkhas_1.Fname + ' ' + Tbl_Ashkhas_1.Lname AS NameMoref, Tbl_Ashkhas_1.CodeMeli AS CodeMeliMoaref, Tbl_Ashkhas_1.id AS CodeMoaref,
                         dbo.Tbl_Ashkhas.Des, dbo.Tbl_Ashkhas.VarizBeMoaref, Tbl_Ashkhas_2.Fname + ' ' + Tbl_Ashkhas_2.Lname AS NameMoref2, Tbl_Ashkhas_2.CodeMeli AS CodeMeliMoaref2, Tbl_Ashkhas_2.id AS CodeMoaref2,
                         dbo.Tbl_Ashkhas.Mizan_Har_Melyoon_Moaref2
FROM            dbo.Tbl_Ashkhas LEFT OUTER JOIN
                         dbo.Tbl_Ashkhas AS Tbl_Ashkhas_2 ON dbo.Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id2 = Tbl_Ashkhas_2.id LEFT OUTER JOIN
                         dbo.Tbl_Ashkhas AS Tbl_Ashkhas_1 ON dbo.Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id = Tbl_Ashkhas_1.id

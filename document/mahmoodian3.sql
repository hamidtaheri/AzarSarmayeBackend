USE [Mahmoodiyan3]
GO
/****** Object:  User [DESKTOP-0P424T6\Administrator]    Script Date: 2/28/2021 9:17:56 PM ******/
CREATE USER [DESKTOP-0P424T6\Administrator] FOR LOGIN [DESKTOP-0P424T6\Administrator] WITH DEFAULT_SCHEMA=[dbo]
GO
ALTER ROLE [db_owner] ADD MEMBER [DESKTOP-0P424T6\Administrator]
GO
/****** Object:  UserDefinedFunction [dbo].[Get_Mande]    Script Date: 2/28/2021 9:17:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
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
return (isnull((select sum(Mablagh) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=1),0)+isnull((select sum(Mablagh) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=3),0)-isnull((select sum(Mablagh) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=2),0)-isnull((select sum(Mablagh) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=4),0)+isnull((select sum(Mablagh) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=5),0))

END
GO
/****** Object:  UserDefinedFunction [dbo].[Get_Mande_By_Date]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE FUNCTION [dbo].[Get_Mande_By_Date](
	@Tbl_Ashkhas_id int,@Tarikh nvarchar(10)
)
RETURNS bigint
AS
BEGIN
return (isnull((select sum(Mablagh*DarMelyoon) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=1 and Tarikh_Moaser<=@Tarikh),0)+isnull((select sum(Mablagh*DarMelyoon) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=3 and Tarikh_Moaser<=@Tarikh),0)-isnull((select sum(Mablagh*DarMelyoon) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=2 and Tarikh_Moaser<=@Tarikh),0)-isnull((select sum(Mablagh*DarMelyoon) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=4 and Tarikh_Moaser<=@Tarikh),0)+isnull((select sum(Mablagh*DarMelyoon) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=5 and Tarikh_Moaser<=@Tarikh),0))/10000000

END
GO
/****** Object:  UserDefinedFunction [dbo].[Get_Mande_By_Date_Moaref]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE FUNCTION [dbo].[Get_Mande_By_Date_Moaref](
	@Tbl_Ashkhas_id int,@Tarikh nvarchar(10)
)
RETURNS bigint
AS
BEGIN
return (isnull((select sum(Mablagh) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=1 and Tarikh_Moaser_Moaref<=@Tarikh),0)+isnull((select sum(Mablagh) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=3 and Tarikh_Moaser_Moaref<=@Tarikh),0)-isnull((select sum(Mablagh) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=2 and Tarikh_Moaser_Moaref<=@Tarikh),0)-isnull((select sum(Mablagh) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=4 and Tarikh_Moaser_Moaref<=@Tarikh),0)+isnull((select sum(Mablagh) from Tbl_Tarakonesh where Tbl_Ashkhas_id=@Tbl_Ashkhas_id and Tbl_Type_Vajh_id=5 and Tarikh_Moaser_Moaref<=@Tarikh),0))

END
GO
/****** Object:  UserDefinedFunction [dbo].[Get_Safte]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
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
return (isnull((select sum(Mablagh) from Tbl_Safte where Tbl_Ashkhas_id=@Tbl_Ashkhas_id ),0))

END
GO
/****** Object:  Table [dbo].[Tbl_Ashkhas]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tbl_Ashkhas](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Fname] [nvarchar](100) NOT NULL,
	[Lname] [nvarchar](100) NULL,
	[CodeMeli] [nvarchar](10) NULL,
	[Adress] [nvarchar](300) NULL,
	[ShomareKart] [nvarchar](16) NULL,
	[Hesab] [nchar](20) NULL,
	[Moaref_Tbl_Ashkhas_id] [int] NULL,
	[Mizan_Har_Melyoon] [int] NOT NULL,
	[Mizan_Har_Melyoon_Moaref] [int] NOT NULL,
	[Daryaft_Sood] [bit] NOT NULL,
	[Des] [nvarchar](300) NULL,
	[VarizBeMoaref] [bit] NOT NULL,
	[MorefiBekhod] [bit] NOT NULL,
	[Kosoorat] [bigint] NOT NULL,
	[Kosoorat_Moarefi] [bigint] NOT NULL,
	[Tel] [nvarchar](15) NULL,
	[Moaref_Tbl_Ashkhas_id2] [int] NULL,
	[Mizan_Har_Melyoon_Moaref2] [int] NOT NULL,
	[MorefiBekhod2] [bit] NOT NULL,
 CONSTRAINT [PK_Tbl_Ashkhas] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tbl_Config]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tbl_Config](
	[Username] [nvarchar](20) NOT NULL,
	[Password] [nvarchar](20) NOT NULL,
 CONSTRAINT [PK_Tbl_Config] PRIMARY KEY CLUSTERED 
(
	[Username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tbl_Pardakht_List]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tbl_Pardakht_List](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Onvan] [nvarchar](100) NOT NULL,
	[Tarikh] [nvarchar](10) NULL,
	[Mah] [nvarchar](10) NULL,
	[Mah_Count] [int] NULL,
	[Des] [nvarchar](200) NULL,
	[Az_Int] [int] NULL,
	[Ta_Int] [int] NULL,
	[louk] [bit] NOT NULL,
 CONSTRAINT [PK_Tbl_Pardakht_List] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tbl_Safte]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tbl_Safte](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Tbl_Ashkhas_id] [int] NOT NULL,
	[Serial] [nvarchar](200) NULL,
	[Mablagh] [bigint] NOT NULL,
	[Tarikh] [nvarchar](10) NOT NULL,
	[Des] [nvarchar](200) NULL,
 CONSTRAINT [PK_Tbl_Safte] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tbl_Tarakonesh]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tbl_Tarakonesh](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Tbl_Ashkhas_id] [int] NOT NULL,
	[Tarikh] [nvarchar](10) NOT NULL,
	[Tarikh_Moaser] [nvarchar](10) NOT NULL,
	[Tarikh_Moaser_Moaref] [nvarchar](10) NOT NULL,
	[Time] [datetime] NOT NULL,
	[Mablagh] [bigint] NOT NULL,
	[Tbl_Type_Vajh_id] [int] NOT NULL,
	[NahveyePardakht] [nvarchar](100) NULL,
	[Des] [nvarchar](300) NULL,
	[Tbl_Pardakht_List_id] [int] NULL,
	[DarMelyoon] [bigint] NOT NULL,
 CONSTRAINT [PK_Tbl_Tarakonesh] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tbl_Type_Vajh]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tbl_Type_Vajh](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](30) NOT NULL,
 CONSTRAINT [PK_Tbl_Type_Vajh] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  UserDefinedFunction [dbo].[getbank_VarizBeMoaref0]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE FUNCTION [dbo].[getbank_VarizBeMoaref0]
(	
	@id int
)
RETURNS TABLE 
AS
RETURN 
(
SELECT         Tbl_Ashkhas.id,SUM(Tbl_Tarakonesh.Mablagh) AS Pardakhti
FROM            Tbl_Ashkhas INNER JOIN
                         Tbl_Tarakonesh ON Tbl_Ashkhas.id = Tbl_Tarakonesh.Tbl_Ashkhas_id
WHERE        (Tbl_Tarakonesh.Tbl_Pardakht_List_id = @id) AND (Tbl_Tarakonesh.Tbl_Type_Vajh_id = 4) and Tbl_Ashkhas.VarizBeMoaref=0
GROUP BY  Tbl_Ashkhas.id
HAVING        (SUM(Tbl_Tarakonesh.Mablagh) > 0)
)
GO
/****** Object:  UserDefinedFunction [dbo].[getbank_VarizBeMoaref1]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create FUNCTION [dbo].[getbank_VarizBeMoaref1]
(	
	@id int
)
RETURNS TABLE 
AS
RETURN 
(
SELECT         Tbl_Ashkhas.id,SUM(Tbl_Tarakonesh.Mablagh) AS Pardakhti,Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id
FROM            Tbl_Ashkhas INNER JOIN
                         Tbl_Tarakonesh ON Tbl_Ashkhas.id = Tbl_Tarakonesh.Tbl_Ashkhas_id
WHERE        (Tbl_Tarakonesh.Tbl_Pardakht_List_id = @id) AND (Tbl_Tarakonesh.Tbl_Type_Vajh_id = 4) and Tbl_Ashkhas.VarizBeMoaref=1
GROUP BY  Tbl_Ashkhas.id,Moaref_Tbl_Ashkhas_id
HAVING        (SUM(Tbl_Tarakonesh.Mablagh) > 0)
)
GO
/****** Object:  UserDefinedFunction [dbo].[getbank]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE FUNCTION [dbo].[getbank]
(	
	@id int
)
RETURNS TABLE 
AS
RETURN 
(
select id,pardakhti as PardakhtiKhod,0 as pardakhti from getbank_VarizBeMoaref0(@id)
union all
select Moaref_Tbl_Ashkhas_id,0 as PardakhtiKhod  ,pardakhti from getbank_VarizBeMoaref1(@id)
)
GO
/****** Object:  UserDefinedFunction [dbo].[getbank_Koli]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
create FUNCTION [dbo].[getbank_Koli]
(	
	@id int
)
RETURNS TABLE 
AS
RETURN 
(
SELECT         Tbl_Ashkhas.id,SUM(Tbl_Tarakonesh.Mablagh) AS Pardakhti,Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id
FROM            Tbl_Ashkhas INNER JOIN
                         Tbl_Tarakonesh ON Tbl_Ashkhas.id = Tbl_Tarakonesh.Tbl_Ashkhas_id
WHERE        (Tbl_Tarakonesh.Tbl_Pardakht_List_id = @id) AND (Tbl_Tarakonesh.Tbl_Type_Vajh_id = 4)
GROUP BY  Tbl_Ashkhas.id,Moaref_Tbl_Ashkhas_id
HAVING        (SUM(Tbl_Tarakonesh.Mablagh) > 0)
)
GO
/****** Object:  View [dbo].[View_AllAshkhas_With_Mande]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
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
GO
SET IDENTITY_INSERT [dbo].[Tbl_Ashkhas] ON 

INSERT [dbo].[Tbl_Ashkhas] ([id], [Fname], [Lname], [CodeMeli], [Adress], [ShomareKart], [Hesab], [Moaref_Tbl_Ashkhas_id], [Mizan_Har_Melyoon], [Mizan_Har_Melyoon_Moaref], [Daryaft_Sood], [Des], [VarizBeMoaref], [MorefiBekhod], [Kosoorat], [Kosoorat_Moarefi], [Tel], [Moaref_Tbl_Ashkhas_id2], [Mizan_Har_Melyoon_Moaref2], [MorefiBekhod2]) VALUES (1, N'رضا', N'عباسی', NULL, NULL, NULL, NULL, 1, 500000, 250000, 1, NULL, 0, 0, 0, 0, NULL, NULL, 350000, 0)
INSERT [dbo].[Tbl_Ashkhas] ([id], [Fname], [Lname], [CodeMeli], [Adress], [ShomareKart], [Hesab], [Moaref_Tbl_Ashkhas_id], [Mizan_Har_Melyoon], [Mizan_Har_Melyoon_Moaref], [Daryaft_Sood], [Des], [VarizBeMoaref], [MorefiBekhod], [Kosoorat], [Kosoorat_Moarefi], [Tel], [Moaref_Tbl_Ashkhas_id2], [Mizan_Har_Melyoon_Moaref2], [MorefiBekhod2]) VALUES (2, N'علی', N'قمی', NULL, NULL, NULL, NULL, NULL, 700000, 0, 1, NULL, 0, 0, 0, 0, NULL, 2, 560000, 0)
INSERT [dbo].[Tbl_Ashkhas] ([id], [Fname], [Lname], [CodeMeli], [Adress], [ShomareKart], [Hesab], [Moaref_Tbl_Ashkhas_id], [Mizan_Har_Melyoon], [Mizan_Har_Melyoon_Moaref], [Daryaft_Sood], [Des], [VarizBeMoaref], [MorefiBekhod], [Kosoorat], [Kosoorat_Moarefi], [Tel], [Moaref_Tbl_Ashkhas_id2], [Mizan_Har_Melyoon_Moaref2], [MorefiBekhod2]) VALUES (3, N'تست', N'رضایی', NULL, NULL, NULL, NULL, NULL, 600000, 0, 1, NULL, 0, 0, 0, 0, NULL, NULL, 0, 0)
SET IDENTITY_INSERT [dbo].[Tbl_Ashkhas] OFF
INSERT [dbo].[Tbl_Config] ([Username], [Password]) VALUES (N'admin', N'admin')
SET IDENTITY_INSERT [dbo].[Tbl_Pardakht_List] ON 

INSERT [dbo].[Tbl_Pardakht_List] ([id], [Onvan], [Tarikh], [Mah], [Mah_Count], [Des], [Az_Int], [Ta_Int], [louk]) VALUES (3, N'تست', N'1399/07/30', N'1399/07/26', 29, N'تست', 5, 29, 0)
SET IDENTITY_INSERT [dbo].[Tbl_Pardakht_List] OFF
SET IDENTITY_INSERT [dbo].[Tbl_Safte] ON 

INSERT [dbo].[Tbl_Safte] ([id], [Tbl_Ashkhas_id], [Serial], [Mablagh], [Tarikh], [Des]) VALUES (1, 2, N';fkrwe;kfs

sfsdfsdfs
fsdfsdfsdf
sdfsdf', 35345435, N'1399/07/08', NULL)
SET IDENTITY_INSERT [dbo].[Tbl_Safte] OFF
SET IDENTITY_INSERT [dbo].[Tbl_Tarakonesh] ON 

INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (38, 1, N'1399/07/01', N'1399/07/01', N'1399/07/01', CAST(N'2020-10-17T00:50:38.263' AS DateTime), 65000000, 1, N'تست', NULL, NULL, 500000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (39, 3, N'1399/07/10', N'1399/07/11', N'1399/07/11', CAST(N'2020-10-17T00:51:08.420' AS DateTime), 45000000, 1, NULL, NULL, NULL, 600000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (40, 2, N'1399/06/26', N'1399/06/27', N'1399/06/27', CAST(N'2020-10-17T00:51:24.803' AS DateTime), 100000000, 1, NULL, NULL, NULL, 700000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (86, 1, N'1399/07/30', N'1399/07/30', N'1399/07/30', CAST(N'2020-10-18T20:50:05.693' AS DateTime), 2708330, 3, N'', N'واريز سود به صندوق', 3, 500000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (87, 1, N'1399/07/30', N'1399/07/30', N'1399/07/30', CAST(N'2020-10-18T20:50:05.693' AS DateTime), 2708330, 4, N'', N'برداشت سود از صندوق', 3, 500000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (88, 1, N'1399/07/30', N'1399/07/30', N'1399/07/30', CAST(N'2020-10-18T20:50:05.697' AS DateTime), 1354170, 5, N'', N' واریز سود معرفی یک رضا عباسی', 3, 250000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (89, 1, N'1399/07/30', N'1399/07/30', N'1399/07/30', CAST(N'2020-10-18T20:50:05.697' AS DateTime), 1354170, 4, N'', N' برداشت سود معرفی یک رضا عباسی', 3, 250000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (90, 2, N'1399/07/30', N'1399/07/30', N'1399/07/30', CAST(N'2020-10-18T20:50:05.700' AS DateTime), 5833330, 3, N'', N'واريز سود به صندوق', 3, 700000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (91, 2, N'1399/07/30', N'1399/07/30', N'1399/07/30', CAST(N'2020-10-18T20:50:05.703' AS DateTime), 5833330, 4, N'', N'برداشت سود از صندوق', 3, 700000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (92, 2, N'1399/07/30', N'1399/07/30', N'1399/07/30', CAST(N'2020-10-18T20:50:05.703' AS DateTime), 4666670, 5, N'', N' واریز سود معرفی دو علی قمی', 3, 560000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (93, 3, N'1399/07/30', N'1399/07/30', N'1399/07/30', CAST(N'2020-10-18T20:50:05.707' AS DateTime), 1710000, 3, N'', N'واريز سود به صندوق', 3, 600000)
INSERT [dbo].[Tbl_Tarakonesh] ([id], [Tbl_Ashkhas_id], [Tarikh], [Tarikh_Moaser], [Tarikh_Moaser_Moaref], [Time], [Mablagh], [Tbl_Type_Vajh_id], [NahveyePardakht], [Des], [Tbl_Pardakht_List_id], [DarMelyoon]) VALUES (94, 3, N'1399/07/30', N'1399/07/30', N'1399/07/30', CAST(N'2020-10-18T20:50:05.707' AS DateTime), 1710000, 4, N'', N'برداشت سود از صندوق', 3, 600000)
SET IDENTITY_INSERT [dbo].[Tbl_Tarakonesh] OFF
SET IDENTITY_INSERT [dbo].[Tbl_Type_Vajh] ON 

INSERT [dbo].[Tbl_Type_Vajh] ([id], [Title]) VALUES (1, N'سپرده گذاری')
INSERT [dbo].[Tbl_Type_Vajh] ([id], [Title]) VALUES (2, N'مرجوع')
INSERT [dbo].[Tbl_Type_Vajh] ([id], [Title]) VALUES (3, N'واریز سود')
INSERT [dbo].[Tbl_Type_Vajh] ([id], [Title]) VALUES (4, N'برداشت سود')
INSERT [dbo].[Tbl_Type_Vajh] ([id], [Title]) VALUES (5, N'واریز سود معرفی')
SET IDENTITY_INSERT [dbo].[Tbl_Type_Vajh] OFF
ALTER TABLE [dbo].[Tbl_Ashkhas] ADD  CONSTRAINT [DF_Tbl_Ashkhas_Mizan_Har_Melyoon]  DEFAULT ((0)) FOR [Mizan_Har_Melyoon]
GO
ALTER TABLE [dbo].[Tbl_Ashkhas] ADD  CONSTRAINT [DF_Tbl_Ashkhas_Mizan_Har_Melyoon1]  DEFAULT ((0)) FOR [Mizan_Har_Melyoon_Moaref]
GO
ALTER TABLE [dbo].[Tbl_Ashkhas] ADD  CONSTRAINT [DF_Tbl_Ashkhas_Daryaft_Sood]  DEFAULT ((1)) FOR [Daryaft_Sood]
GO
ALTER TABLE [dbo].[Tbl_Ashkhas] ADD  CONSTRAINT [DF_Tbl_Ashkhas_VarizBeMoaref]  DEFAULT ((0)) FOR [VarizBeMoaref]
GO
ALTER TABLE [dbo].[Tbl_Ashkhas] ADD  CONSTRAINT [DF_Tbl_Ashkhas_MorefiBekhod]  DEFAULT ((0)) FOR [MorefiBekhod]
GO
ALTER TABLE [dbo].[Tbl_Ashkhas] ADD  CONSTRAINT [DF_Tbl_Ashkhas_Kosoorat]  DEFAULT ((0)) FOR [Kosoorat]
GO
ALTER TABLE [dbo].[Tbl_Ashkhas] ADD  CONSTRAINT [DF_Tbl_Ashkhas_Kosoorat_Moarefi]  DEFAULT ((0)) FOR [Kosoorat_Moarefi]
GO
ALTER TABLE [dbo].[Tbl_Ashkhas] ADD  CONSTRAINT [DF_Tbl_Ashkhas_Mizan_Har_Melyoon_Moaref1]  DEFAULT ((0)) FOR [Mizan_Har_Melyoon_Moaref2]
GO
ALTER TABLE [dbo].[Tbl_Ashkhas] ADD  CONSTRAINT [DF_Tbl_Ashkhas_MorefiBekhod1]  DEFAULT ((0)) FOR [MorefiBekhod2]
GO
ALTER TABLE [dbo].[Tbl_Pardakht_List] ADD  CONSTRAINT [DF_Tbl_Pardakht_List_Mah_Count]  DEFAULT ((30)) FOR [Mah_Count]
GO
ALTER TABLE [dbo].[Tbl_Pardakht_List] ADD  CONSTRAINT [DF_Tbl_Pardakht_List_Az_Int]  DEFAULT ((1)) FOR [Az_Int]
GO
ALTER TABLE [dbo].[Tbl_Pardakht_List] ADD  CONSTRAINT [DF_Tbl_Pardakht_List_Ta_Int]  DEFAULT ((30)) FOR [Ta_Int]
GO
ALTER TABLE [dbo].[Tbl_Pardakht_List] ADD  CONSTRAINT [DF_Tbl_Pardakht_List_louk]  DEFAULT ((0)) FOR [louk]
GO
ALTER TABLE [dbo].[Tbl_Safte] ADD  CONSTRAINT [DF_Tbl_Safte_Mablagh]  DEFAULT ((0)) FOR [Mablagh]
GO
ALTER TABLE [dbo].[Tbl_Tarakonesh] ADD  CONSTRAINT [DF_Tbl_Tarakonesh_Mablagh]  DEFAULT ((0)) FOR [Mablagh]
GO
ALTER TABLE [dbo].[Tbl_Tarakonesh] ADD  CONSTRAINT [DF_Tbl_Tarakonesh_Price]  DEFAULT ((0)) FOR [DarMelyoon]
GO
ALTER TABLE [dbo].[Tbl_Ashkhas]  WITH CHECK ADD  CONSTRAINT [FK_Tbl_Ashkhas_Tbl_Ashkhas] FOREIGN KEY([Moaref_Tbl_Ashkhas_id])
REFERENCES [dbo].[Tbl_Ashkhas] ([id])
GO
ALTER TABLE [dbo].[Tbl_Ashkhas] CHECK CONSTRAINT [FK_Tbl_Ashkhas_Tbl_Ashkhas]
GO
ALTER TABLE [dbo].[Tbl_Safte]  WITH CHECK ADD  CONSTRAINT [FK_Tbl_Safte_Tbl_Safte] FOREIGN KEY([Tbl_Ashkhas_id])
REFERENCES [dbo].[Tbl_Ashkhas] ([id])
GO
ALTER TABLE [dbo].[Tbl_Safte] CHECK CONSTRAINT [FK_Tbl_Safte_Tbl_Safte]
GO
ALTER TABLE [dbo].[Tbl_Tarakonesh]  WITH CHECK ADD  CONSTRAINT [FK_Tbl_Tarakonesh_Tbl_Ashkhas] FOREIGN KEY([Tbl_Ashkhas_id])
REFERENCES [dbo].[Tbl_Ashkhas] ([id])
GO
ALTER TABLE [dbo].[Tbl_Tarakonesh] CHECK CONSTRAINT [FK_Tbl_Tarakonesh_Tbl_Ashkhas]
GO
ALTER TABLE [dbo].[Tbl_Tarakonesh]  WITH CHECK ADD  CONSTRAINT [FK_Tbl_Tarakonesh_Tbl_Pardakht_List] FOREIGN KEY([Tbl_Pardakht_List_id])
REFERENCES [dbo].[Tbl_Pardakht_List] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Tbl_Tarakonesh] CHECK CONSTRAINT [FK_Tbl_Tarakonesh_Tbl_Pardakht_List]
GO
ALTER TABLE [dbo].[Tbl_Tarakonesh]  WITH CHECK ADD  CONSTRAINT [FK_Tbl_Tarakonesh_Tbl_Tarakonesh] FOREIGN KEY([id])
REFERENCES [dbo].[Tbl_Tarakonesh] ([id])
GO
ALTER TABLE [dbo].[Tbl_Tarakonesh] CHECK CONSTRAINT [FK_Tbl_Tarakonesh_Tbl_Tarakonesh]
GO
ALTER TABLE [dbo].[Tbl_Tarakonesh]  WITH CHECK ADD  CONSTRAINT [FK_Tbl_Tarakonesh_Tbl_Type_Vajh] FOREIGN KEY([Tbl_Type_Vajh_id])
REFERENCES [dbo].[Tbl_Type_Vajh] ([id])
GO
ALTER TABLE [dbo].[Tbl_Tarakonesh] CHECK CONSTRAINT [FK_Tbl_Tarakonesh_Tbl_Type_Vajh]
GO
/****** Object:  StoredProcedure [dbo].[All_Calcs]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[All_Calcs]
	@Tbl_Pardakht_List_Id int,@countm int
AS
BEGIN
	delete from Tbl_Tarakonesh where Tbl_Tarakonesh.Tbl_Pardakht_List_id=@Tbl_Pardakht_List_Id 

	declare @_id int
	DECLARE the_cursor CURSOR FAST_FORWARD
FOR SELECT [id]
  FROM Tbl_Ashkhas
  	
OPEN the_cursor
FETCH NEXT FROM the_cursor INTO @_id

WHILE @@FETCH_STATUS = 0
BEGIN

EXEC	[dbo].[Pardakht_Calc_Skhakhs]
		@Tbl_Pardakht_List_Id = @Tbl_Pardakht_List_Id,
		@id_Shakhs = @_id,@countmah=@countm

FETCH NEXT FROM the_cursor INTO @_id
END

CLOSE the_cursor
DEALLOCATE the_cursor

END
GO
/****** Object:  StoredProcedure [dbo].[Pardakht_Calc_Skhakhs]    Script Date: 2/28/2021 9:17:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[Pardakht_Calc_Skhakhs]
	@Tbl_Pardakht_List_Id int,@id_Shakhs int,@countmah int
AS
BEGIN

declare @varibekhod bit=(select  MorefiBekhod from Tbl_Ashkhas where Tbl_Ashkhas.id=@id_Shakhs)
declare @varibekhod2 bit=(select  MorefiBekhod2 from Tbl_Ashkhas where Tbl_Ashkhas.id=@id_Shakhs)
declare @mz decimal(18,4)=(select  Mizan_Har_Melyoon from Tbl_Ashkhas where Tbl_Ashkhas.id=@id_Shakhs)
declare @mz_m decimal(18,4)=(select  Mizan_Har_Melyoon_Moaref from Tbl_Ashkhas where Tbl_Ashkhas.id=@id_Shakhs)
declare @m_id int=(select  Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id from Tbl_Ashkhas where Tbl_Ashkhas.id=@id_Shakhs)

declare @mz_m2 decimal(18,4)=(select  Mizan_Har_Melyoon_Moaref2 from Tbl_Ashkhas where Tbl_Ashkhas.id=@id_Shakhs)
declare @m_id2 int=(select  Tbl_Ashkhas.Moaref_Tbl_Ashkhas_id2 from Tbl_Ashkhas where Tbl_Ashkhas.id=@id_Shakhs)


Declare @az int
Declare @ta int
set @az=(select Az_Int from Tbl_Pardakht_List where id=@Tbl_Pardakht_List_Id)
set @ta=(select Ta_Int from Tbl_Pardakht_List where id=@Tbl_Pardakht_List_Id)
declare @mahcount decimal(18,4)=(select Mah_Count from Tbl_Pardakht_List where id=@Tbl_Pardakht_List_Id)
declare @pdate nvarchar(10)=(select Mah from Tbl_Pardakht_List where id=@Tbl_Pardakht_List_Id)

declare @tarikh nvarchar(10)=(select Tarikh from Tbl_Pardakht_List where id=@Tbl_Pardakht_List_Id)
declare @d nvarchar(10)
declare @sood decimal(18,4)=0
declare @sood_Moref decimal(18,4)=0
declare @sood_Moref2 decimal(18,4)=0


declare @kosoorat bigint=(select  Kosoorat from Tbl_Ashkhas where Tbl_Ashkhas.id=@id_Shakhs)





while @az<=@ta
begin
set @d=SUBSTRING(@pdate,0,9)+RIGHT('00'+cast(@az as nvarchar(2)),2)


--print @d

declare  @remian decimal(18,4)
set @remian=dbo.Get_Mande_By_Date(@id_Shakhs,@d)
--print @remian

set @sood=@sood+(((@remian))/@countmah)
print @sood



--
--print @sood_Moref
set @az=@az+1
end


set @az=(select Az_Int from Tbl_Pardakht_List where id=@Tbl_Pardakht_List_Id)
set @ta=(select Ta_Int from Tbl_Pardakht_List where id=@Tbl_Pardakht_List_Id)


while @az<=@ta
begin
set @d=SUBSTRING(@pdate,0,9)+RIGHT('00'+cast(@az as nvarchar(2)),2)


--print @d

declare  @remian_moaref decimal(18,4)
set @remian_moaref=dbo.Get_Mande_By_Date_Moaref(@id_Shakhs,@d)
--print @remian



set @sood_Moref=@sood_Moref+((((@remian_moaref/10000000)*@mz_m))/@countmah)
set @sood_Moref2=@sood_Moref2+((((@remian_moaref/10000000)*@mz_m2))/@countmah)


--
--print @sood_Moref
set @az=@az+1
end











		declare @sood_b bigint =cast(round(@sood,-1) as bigint)
		declare @sood_Moref_b bigint =cast(round(@sood_Moref,-1) as bigint)
		declare @sood_Moref_b2 bigint =cast(round(@sood_Moref2,-1) as bigint)








if(@kosoorat>0)
begin

set @sood_b=@sood_b-@kosoorat
update Tbl_Ashkhas set Kosoorat=0 where Tbl_Ashkhas.id=@id_Shakhs
end





if(@sood_b>0)
begin


INSERT INTO [dbo].[Tbl_Tarakonesh]
           ([Tbl_Ashkhas_id]
           ,[Tarikh],[Tarikh_Moaser],[Tarikh_Moaser_Moaref]
           ,[Time]
           ,[Mablagh]
           ,[Tbl_Type_Vajh_id]
           ,[NahveyePardakht]
           ,[Des]
           ,[Tbl_Pardakht_List_id],[DarMelyoon])values(@id_Shakhs,@tarikh,@tarikh,@tarikh,getdate(),@sood_b,3,'','واریز سود به صندوق',@Tbl_Pardakht_List_Id,@mz)

		   if((select  Daryaft_Sood from Tbl_Ashkhas where Tbl_Ashkhas.id=@id_Shakhs)=1)
begin

INSERT INTO [dbo].[Tbl_Tarakonesh]
           ([Tbl_Ashkhas_id]
           ,[Tarikh],[Tarikh_Moaser],[Tarikh_Moaser_Moaref]
           ,[Time]
           ,[Mablagh]
           ,[Tbl_Type_Vajh_id]
           ,[NahveyePardakht]
           ,[Des]
           ,[Tbl_Pardakht_List_id],[DarMelyoon])values(@id_Shakhs,@tarikh,@tarikh,@tarikh,getdate(),@sood_b,4,'','برداشت سود از صندوق',@Tbl_Pardakht_List_Id,@mz)
	
		   end
end		   
if(@sood_Moref_b>0 and @m_id is not null)
begin
declare @idd int
if(@varibekhod=1)
begin
set @idd=@id_Shakhs
end
else
begin
set @idd=@m_id
end



declare @Kosoorat_Moarefi bigint=(select  Kosoorat_Moarefi from Tbl_Ashkhas where Tbl_Ashkhas.id=@idd)

if(@Kosoorat_Moarefi>0)
begin
set @sood_Moref_b=@sood_Moref_b-@Kosoorat_Moarefi
update Tbl_Ashkhas set Kosoorat_Moarefi=0 where Tbl_Ashkhas.id=@idd
end



declare @name1 nvarchar(100)=(select Fname + ' ' + Lname from Tbl_Ashkhas where id=@id_Shakhs)
INSERT INTO [dbo].[Tbl_Tarakonesh]
           ([Tbl_Ashkhas_id]
           ,[Tarikh],[Tarikh_Moaser],[Tarikh_Moaser_Moaref]
           ,[Time]
           ,[Mablagh]
           ,[Tbl_Type_Vajh_id]
           ,[NahveyePardakht]
           ,[Des]
           ,[Tbl_Pardakht_List_id],[DarMelyoon])values(@idd,@tarikh,@tarikh,@tarikh,getdate(),@sood_Moref_b,5,'',N' واریز سود معرفی یک '+@name1,@Tbl_Pardakht_List_Id,@mz_m)



		   if((select  Daryaft_Sood from Tbl_Ashkhas where Tbl_Ashkhas.id=@m_id)=1)
begin

INSERT INTO [dbo].[Tbl_Tarakonesh]
           ([Tbl_Ashkhas_id]
           ,[Tarikh],[Tarikh_Moaser],[Tarikh_Moaser_Moaref]
           ,[Time]
           ,[Mablagh]
           ,[Tbl_Type_Vajh_id]
           ,[NahveyePardakht]
           ,[Des]
           ,[Tbl_Pardakht_List_id],[DarMelyoon])values(@idd,@tarikh,@tarikh,@tarikh,getdate(),@sood_Moref_b,4,'',N' برداشت سود معرفی یک '+@name1,@Tbl_Pardakht_List_Id,@mz_m)
		   end






end



















if(@sood_Moref_b2>0 and @m_id2 is not null)
begin
declare @idd2 int
if(@varibekhod2=1)
begin
set @idd2=@id_Shakhs
end
else
begin
set @idd2=@m_id2
end



declare @Kosoorat_Moarefi2 bigint=(select  Kosoorat_Moarefi from Tbl_Ashkhas where Tbl_Ashkhas.id=@idd)

if(@Kosoorat_Moarefi>0)
begin
set @sood_Moref_b2=@sood_Moref_b2-@Kosoorat_Moarefi
update Tbl_Ashkhas set Kosoorat_Moarefi=0 where Tbl_Ashkhas.id=@idd
end



declare @name2 nvarchar(100)=(select Fname + ' ' + Lname from Tbl_Ashkhas where id=@id_Shakhs)
INSERT INTO [dbo].[Tbl_Tarakonesh]
           ([Tbl_Ashkhas_id]
           ,[Tarikh],[Tarikh_Moaser],[Tarikh_Moaser_Moaref]
           ,[Time]
           ,[Mablagh]
           ,[Tbl_Type_Vajh_id]
           ,[NahveyePardakht]
           ,[Des]
           ,[Tbl_Pardakht_List_id],[DarMelyoon])values(@idd2,@tarikh,@tarikh,@tarikh,getdate(),@sood_Moref_b2,5,'',N' واریز سود معرفی دو '+@name2,@Tbl_Pardakht_List_Id,@mz_m2)



		   if((select  Daryaft_Sood from Tbl_Ashkhas where Tbl_Ashkhas.id=@m_id)=1)
begin

INSERT INTO [dbo].[Tbl_Tarakonesh]
           ([Tbl_Ashkhas_id]
           ,[Tarikh],[Tarikh_Moaser],[Tarikh_Moaser_Moaref]
           ,[Time]
           ,[Mablagh]
           ,[Tbl_Type_Vajh_id]
           ,[NahveyePardakht]
           ,[Des]
           ,[Tbl_Pardakht_List_id],[DarMelyoon])values(@idd2,@tarikh,@tarikh,@tarikh,getdate(),@sood_Moref_b2,4,'',N' برداشت سود معرفی دو '+@name2,@Tbl_Pardakht_List_Id,@mz_m2)
		   end






end


END
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[20] 2[20] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "Tbl_Ashkhas"
            Begin Extent = 
               Top = 6
               Left = 38
               Bottom = 337
               Right = 290
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "Tbl_Ashkhas_2"
            Begin Extent = 
               Top = 81
               Left = 600
               Bottom = 288
               Right = 846
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "Tbl_Ashkhas_1"
            Begin Extent = 
               Top = 35
               Left = 358
               Bottom = 226
               Right = 604
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
      Begin ColumnWidths = 19
         Width = 284
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 2220
         Width = 1500
         Width = 1500
         Width = 1500
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1440
         Alias = 900
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'View_AllAshkhas_With_Mande'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'View_AllAshkhas_With_Mande'
GO
